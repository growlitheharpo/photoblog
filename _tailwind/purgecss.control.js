const Purgecss = require('purgecss')
const fs = require('fs')
const path = require('path')

const outputDir = path.join(__dirname, '../assets/css')

const purgecss = new Purgecss({
    css: ['../assets/css/output.css'],
    content: [ '../*.html', '../**/*.html' ],
    // Use the extractor from Tailwind: https://tailwindcss.com/docs/controlling-file-size/
    defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
})

const result = purgecss.purge()

result.forEach(out => {
	const filePath = out.file.split('/')
	fs.writeFileSync(`${outputDir}/${filePath[filePath.length - 1]}`, out.css, 'utf-8')
})

console.log('Done')
