
# Markdown test

## Table of Contents

[[toc]]

## Alert

- success
  
  ::: success
  Hello world! [Link](#).
  :::
  
- info
  
  ::: info
  Hello world! [Link](#).
  :::
  
- warning
  
  ::: warning
  Hello world! [Link](#).
  :::
  
- danger
  
  ::: danger
  Hello world! [Link](#).
  :::

## Footnote

Here is a footnote reference,[^1] and another.[^longnote]

[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.
    Subsequent paragraphs are indented to show that theybelong to the previous footnote.

## Mermaid
  
  ```mermaid
  graph LR
      A-->B;
      B-->C1;
      B-->C2;
      C1-->D;
      C2-->D;
  ```

## Math
  
$$$
P(A | B) = (P(B | A)P(A)) / P(B)
$$$

## YouTube

@[youtube](lJIrF4YjHfQ)

## Headings

# h1 Heading

## h2 Heading

### h3 Heading

#### h4 Heading

##### h5 Heading

###### h6 Heading

## Text emphasis

_italic_

~~strikethrough~~

__bold__

___bold and italic___

==highlight==

## Link

### Named links

[google](https://www.google.com/)

### URL

https://www.google.com/

## Table

| Header 01 | Header 02 |
|----------- | ---------- |
| Contents11 | Contents12 |
| Contents21 | Contents22 |

## List

### Unordered list

- A
  - A1
  - A2
    - A1-1
- B

### Ordered list

1. A
   1. A1
   2. A2
      1. A1-1
2. B

### Check list

- [ ] A
- [x] B
- [ ] C

## Description list

Name 1

:   Def1A
Def1B

Name2 *Name Markup*

:   Def2

## Reference

> Reference A
>> Reference AA
>>> Reference AAA

> Reference B

## Image

![Img Alt](https://picsum.photos/200/50 "Img Title")

## Horizon line

---

## Cord

### JavaScript

``` js
var foo = function (bar) {
    return bar++;
};

console.log(foo(5));
```

### Python

```python
def foo(bar):
  return bar+=1

print(foo(5))
```

## HTML converter for server created

https://github.com/Eruhitsuji/XMLandMD2HTMLConverter

This project allows you to convert from XML to HTML, including HTML and Markdown.

## Special character

The three symbols <,>," will eventually be converted and may not be displayed in this project.
The same applies to the special characters ```&rt_lt;```, ```&rt_gt;```, and ```&rt_quot;``` in HTML.
To solve those cases, try prefixing the sign with "rt_" and assigning ```&rrt_lt;```, ```&rrt_gt;``` and ```&rrt_quot;```.
