<h3>append data</h3>
<div>
    <p>
        append 01
    </p>
    <li>
        <span style='color:red;'>abc</span>
    </li>
    <li>
        &lt;span style='color:red;'&gt;abc&lt;/span&gt;
    </li>
    <li>
        &rt_lt;span style='color:red;'&rt_gt;abc&rt_lt;/span&rt_gt;
    </li>
    <li>
        &rt_quot;abc&rt_quot;
    </li>
    
    <p>
        append 02
    </p>
</div>
    
<table>
    <tr>
        <th class="bottom_bold">A</th>
        <th class="bottom_bold">B</th>
        <th class="bottom_bold">C</th>
    </tr>
    <tr>
        <td>a01</td>
        <td>b01</td>
        <td>c01</td>
    </tr>
    <tr>
        <td class="bottom_double">a02</td>
        <td>b02</td>
        <td class="bottom_dashed">c02</td>
    </tr>
    <tr>
        <td>a03</td>
        <td>b03</td>
        <td>c03</td>
    </tr>
    <tr>
        <td class="bottom_double">a04</td>
        <td class="bottom_double">b04</td>
        <td class="bottom_double">c04</td>
    </tr>
    <tr>
        <td>a05</td>
        <td>b05</td>
        <td>c05</td>
    </tr>
    <tr>
        <td class="bottom_dashed">a06</td>
        <td class="bottom_dashed">b06</td>
        <td class="bottom_dashed">c06</td>
    </tr>
    <tr>
        <td>a07</td>
        <td>b07</td>
        <td>c07</td>
    </tr>
</table>

<h4>PHP test</h4>
<?php
$n=10;
echo("<p>php test2</p>");
print_r($n);
?>