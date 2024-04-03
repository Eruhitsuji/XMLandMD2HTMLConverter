# XMLandMD2HTMLConverter

This program can convert XML data written in a mixture of HTML and Markdown into normal static HTML.
To convert from Markdown to HTML, [markdown-it](https://github.com/markdown-it/markdown-it) was used.

## Prerequisite environment

- Node.js related
- Python3 and above

## Installation of relevant libraries

```bash
npm install package.json
pip install -r requirements.txt
```

## How to run

Before running, configure the input and output settings in [upload_config.json](upload_config.json).

Also change [converter_config.json](converter_config.json) if necessary.
For example, by changing "default_suffix" from "html" to "php", the output can be set to PHP file.

Then execute upload.py.

```bash
python3 upload.py
```

## Sample of this project

The output for [input directory](input) is [output directory](output).
Also, a sample output page is [here](https://eruhitsuji.github.io/XMLandMD2HTMLConverter/output/test/test.html).
