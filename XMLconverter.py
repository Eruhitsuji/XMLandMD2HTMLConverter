import os
import json
from pathlib import Path
import shutil
from bs4 import BeautifulSoup
from subprocess import Popen
import datetime
import platform
import glob
import xml.etree.ElementTree as ET
import urllib.request, urllib.error

class XMLconverter():
    settings=json.load(open("converter_config.json",mode="r",encoding="utf-8"))


    PAGE_CONFIG_TAG=settings["page_config_tag"]
    RAW_DATA_TAG=settings["raw_data_tag"]
    MD_DATA_TAG=settings["md_data_tag"]
    SP_TAG=settings["sp_tag"]

    TMP_DIR=settings["tmp_dir"]
    TMP_MD_FILE=settings["tmp_md_file"]
    TMP_HTML_FILE=settings["tmp_html_file"]

    DEFAULT_SUFFIX=settings["default_suffix"]


    def allRemoveDir(dir):
        if(os.path.isdir(dir)):
            shutil.rmtree(dir)

    def changeSuffix(p,new_suffix):
        pp=Path(p)
        return Path(Path(pp.parent)/Path(str(pp.stem)+"."+new_suffix))
        

    def Tag2String(tag):
        ts=str(tag)
        s="<{name}>".format(name=tag.name)
        e="</{name}>".format(name=tag.name)
        ts=ts.replace(s,"")
        ts=ts.replace(e,"")
        return ts

    def replaceHTMLSPChar(text:str):
        replace_list=[
            ("gt",">"),
            ("lt","<"),
            ("quot","\""),
        ]

        for r in replace_list:
            ssp="&rrt_{};".format(r[0])
            sp="&rt_{};".format(r[0])
            before="&{};".format(r[0])
            after=r[1]

            text=text.replace(before,after)
            text=text.replace(sp,before)
            text=text.replace(ssp,sp)
        return text


    def MD2HTML(dc):
        dc=XMLconverter.replaceHTMLSPChar(dc)

        XMLconverter.allRemoveDir(XMLconverter.TMP_DIR)
        os.makedirs(XMLconverter.TMP_DIR,exist_ok=True)
        with open(XMLconverter.TMP_DIR+XMLconverter.TMP_MD_FILE,mode="w",encoding="utf-8") as f:
            f.write(dc)
        
        cmd=["node","index.js",XMLconverter.TMP_DIR+XMLconverter.TMP_MD_FILE,XMLconverter.TMP_DIR+XMLconverter.TMP_HTML_FILE]
        popen = Popen(" ".join(cmd),shell=True)
        popen.wait()
        
        with open(XMLconverter.TMP_DIR+XMLconverter.TMP_HTML_FILE,mode="r",encoding="utf-8") as f:
            dch=f.read()
        XMLconverter.allRemoveDir(XMLconverter.TMP_DIR)
        return dch   


    def path2updateDate(path:Path):
        return datetime.datetime.fromtimestamp(path.stat().st_mtime)

    def creation_date(path:Path):
        if(platform.system()=="Windows"):
            return os.path.getctime(path)
        else:
            stat=os.stat(path)
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime

    def path2createDate(path:Path):
        return datetime.datetime.fromtimestamp(XMLconverter.creation_date(path))

    def setTitle(r_dict:dict,out_text:str,title:str):
        out_text+="<script>(function(t_str='"+title+"'){document.title=t_str;}());</script>"
        r_dict["title"]=title
        return (r_dict,out_text)


    def checkURL(url):
        try:
            f=urllib.request.urlopen(url)
            t=f.read().decode()
            f.close()
            return (True,t)
        except:
            return (False,None)

    def readFile(input,input_base_dir=""):
        url_flag,url_text=XMLconverter.checkURL(input)
        if(url_flag):
            return url_text
        else:
            with open(Path(Path(input_base_dir)/Path(input)),mode="r",encoding="utf-8") as f:
                text=f.read()
            return text


    def XML2HTML(input,input_base_dir="",out_base_dir=""):
        r_dict={}

        # setting output path
        output=XMLconverter.changeSuffix(input,XMLconverter.DEFAULT_SUFFIX)
        out_base_dir=Path(out_base_dir)
        out_text=""

        # get input file
        input_path=Path(Path(input_base_dir)/Path(input))
        with open(input_path,mode="r",encoding="utf-8") as f:
            raw_text=f.read()
        
        # get the date of the input file
        create_date=XMLconverter.path2createDate(input_path)
        update_date=XMLconverter.path2updateDate(input_path)
        
        r_dict["create_date"]=create_date
        r_dict["update_date"]=update_date

        # main process
        soup = BeautifulSoup(raw_text, 'html.parser')
        for d in soup.findAll([XMLconverter.PAGE_CONFIG_TAG,XMLconverter.RAW_DATA_TAG,XMLconverter.MD_DATA_TAG,XMLconverter.SP_TAG]):
            d_a=d.attrs
            print(d.name,d_a)
            dc=XMLconverter.replaceHTMLSPChar(XMLconverter.Tag2String(d))
            
            if(d.name==XMLconverter.PAGE_CONFIG_TAG):
                if("out_base_dir" in d_a):
                    out_base_dir=Path(d["out_base_dir"])
                if("out_dir" in d_a):
                    output=Path(Path(d["out_dir"])/Path(str(output.name)))
                if("filename" in d_a):
                    output=Path(Path(output.parent)/Path(d["filename"]))
                if("title" in d_a):
                    (r_dict,out_text)=XMLconverter.setTitle(r_dict,out_text,d_a["title"])
                if("priority" in d_a):
                    r_dict["priority"]=d_a["priority"]

            elif(d.name==XMLconverter.MD_DATA_TAG):
                out_text+=XMLconverter.MD2HTML(dc)+"\n"

            elif(d.name==XMLconverter.RAW_DATA_TAG):
                out_text+=dc+"\n"

            elif(d.name==XMLconverter.SP_TAG):
                if("text" in d_a):
                    out_text+=d["text"]+"\n"
                
                if("input_raw_data" in d_a):
                    out_text+=XMLconverter.readFile(d["input_raw_data"],input_base_dir=input_base_dir)+"\n"
                
                if("input_md_data" in d_a):        
                    out_text+=XMLconverter.MD2HTML(XMLconverter.readFile(d["input_md_data"],input_base_dir=input_base_dir))+"\n"
                
                if("rename_title" in d_a):
                    (r_dict,out_text)=XMLconverter.setTitle(r_dict,out_text,d_a["rename_title"])

                if("disp_create_date" in d_a):
                    df=d["disp_create_date"]
                    if(df=="0"):
                        df="%Y%m%d%H%M%S"
                    ds=create_date.strftime(df)

                    out_text+="<div class='system_date disp_create_date'>{ds}</div>".format(ds=ds)
                
                if("disp_update_date" in d_a):
                    df=d["disp_update_date"]
                    if(df=="0"):
                        df="%Y%m%d%H%M%S"
                    ds=update_date.strftime(df)
                    
                    out_text+="<div class='system_date disp_update_date'>{ds}</div>".format(ds=ds)    

        #out_text=XMLconverter.replaceHTMLSPChar(out_text)
        
        # output
        output_path=Path(out_base_dir/output)
        r_dict["path"]=output
        print("output file :: ",output_path)
        os.makedirs(output_path.parent,exist_ok=True)
        with open(output_path,mode="w",encoding="utf-8") as f:
            f.write(out_text)

        return r_dict

class SiteMap():
    def __init__(self,page_list:list,domain:str=""):
        self.page_list=page_list
        self.domain="" if domain=="" else domain if domain[-1]=="/" else domain+"/"
    
    def outDict(self):
        r=[]
        for page in self.page_list:
            tmp={
                "loc":self.domain+str(page["path"]),
                "page_title":page.get("title","None Title"),
                "lastmod":page["update_date"].strftime("%Y-%m-%d"),
                "priority":float(page.get("priority",1)),
            }
            if(tmp["priority"]>=0):
                r.append(tmp)
        return r

    def createXML(self,xml_path:str):
        DEFAULT_XMLNS="http://www.sitemaps.org/schemas/sitemap/0.9"
        
        urlset=ET.Element("urlset")
        urlset.set("xmlns",DEFAULT_XMLNS)
        tree=ET.ElementTree(element=urlset)

        for page in self.outDict():

            if(page["priority"]>=0):

                url_element=ET.SubElement(urlset,"url")
                
                loc=ET.SubElement(url_element,"loc")
                loc.text=page["loc"]
                
                lastmod=ET.SubElement(url_element,"lastmod")
                lastmod.text=page["lastmod"]

                priority=ET.SubElement(url_element,"priority")
                priority.text=str(page["priority"])

        tree.write(xml_path,encoding="utf-8",xml_declaration=True)
    
    def createJSON(self,json_path:str):
        with open(json_path,mode="w",encoding="utf-8") as f:
	        json.dump(self.outDict(),f,ensure_ascii=False,indent=4)

class Upload():
    settings=json.load(open("upload_config.json",mode="r",encoding="utf-8"))
    
    INPUT_BASE_DIR=settings.get("input_base_dir","")
    INPUT_XML_GLOB_LIST=settings.get("input_xml_glob_list",[])
    EXCLUDE_INPUT_XML_GLOB_LIST=settings.get("exclude_input_xml_glob_list",[])
    INPUT_COPY_DATA_GLOB_LIST=settings.get("input_copy_data_glob_list",[])
    EXCLUDE_INPUT_COPY_DATA_GLOB_LIST=settings.get("exclude_input_copy_data_glob_list",[])
    OUTPUT_BASE_DIR=settings.get("output_base_dir","")

    DOMAIN=settings.get("domain","")
    SITEMAP_XML_PATH=settings.get("sitemap_xml_path","")
    SITEMAP_JSON_PATH=settings.get("sitemap_json_path","")

    def findFile(glob_str_list,exclude_glob_str_list=[],base_dir=""):
        s_pwd=Path.cwd()
        os.chdir(base_dir)
        
        #find exclude file
        exclude_glob_list=[]
        for e_glob_str in exclude_glob_str_list:
            egf=glob.glob(e_glob_str,recursive=True)
            exclude_glob_list+=egf
        
        #find file
        r=[]
        for glob_str in glob_str_list:
            g=glob.glob(glob_str,recursive=True)
            for gf in g: 
                if(gf not in exclude_glob_list):
                    r.append(gf)
        os.chdir(s_pwd)
        return r

    def upload():
        xml_list=Upload.findFile(Upload.INPUT_XML_GLOB_LIST,Upload.EXCLUDE_INPUT_XML_GLOB_LIST,Upload.INPUT_BASE_DIR)

        page_list=[]

        for xml_path in xml_list:
            d=XMLconverter.XML2HTML(xml_path,Upload.INPUT_BASE_DIR,Upload.OUTPUT_BASE_DIR)
            page_list.append(d)

        copy_data_list=Upload.findFile(Upload.INPUT_COPY_DATA_GLOB_LIST,Upload.EXCLUDE_INPUT_COPY_DATA_GLOB_LIST,Upload.INPUT_BASE_DIR)

        for copy_data in copy_data_list:
            input_path=Path(Path(Upload.INPUT_BASE_DIR)/Path(copy_data))
            output_path=Path(Path(Upload.OUTPUT_BASE_DIR)/Path(copy_data))
            if(input_path.is_file()):
                os.makedirs(str(output_path.parent),exist_ok=True)
                shutil.copy2(input_path,output_path)
        
        site_map=SiteMap(page_list,Upload.DOMAIN)
        if(Upload.SITEMAP_XML_PATH!=""):
            site_map.createXML(Path(Path(Upload.OUTPUT_BASE_DIR)/Path(Upload.SITEMAP_XML_PATH)))
        if(Upload.SITEMAP_JSON_PATH!=""):
            site_map.createJSON(Path(Path(Upload.OUTPUT_BASE_DIR)/Path(Upload.SITEMAP_JSON_PATH)))
