const { promisify } = require('util');
const path = require('path');
const fs = require('fs');
const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);
const md = require('markdown-it')({
    linkify: true,
});

/*
const emoji = require('markdown-it-emoji');
const twemoji = require('twemoji')

md.use(emoji);
md.renderer.rules.emoji = function (token, idx) {
    return twemoji.parse(token[idx].content);
};
*/

const footnote = require('markdown-it-footnote');
md.use(footnote);

const mark = require('markdown-it-mark');
md.use(mark);

const deflist = require('markdown-it-deflist');
md.use(deflist);


const mdItMermaid = require('md-it-mermaid');
md.use(mdItMermaid)

const mdItAnchor = require('markdown-it-anchor').default;
md.use(mdItAnchor, {
    level: 2,
    permalink: true,
})

const mdItToc = require('markdown-it-table-of-contents');
md.use(mdItToc, {
    includeLevel: [2, 3, 4],
})

const mdItAlerts = require('markdown-it-alerts');
md.use(mdItAlerts)

const mdItMath = require('markdown-it-math');
md.use(mdItMath)

const mdItBlockEmbed = require('markdown-it-block-embed');
md.use(mdItBlockEmbed, {
    containerClassName: "video-embed",
});



async function mdConverter(input, output) {
    try {
        const markdown = await readFile(input, 'utf-8');
        const html = md.render(markdown);
        await writeFile(output, html);
        console.info('file created successfully');
    } catch (e) {
        console.error('file error', e);
    } 
}

const args = process.argv.slice(2);
const input = path.resolve(__dirname, args[0]);
const output = path.resolve(__dirname, args[1]);
mdConverter(input, output);
