const fs = require('fs').promises; // <-- Changed: Now using the promise-based fs API
const path = require('path');      // <-- Changed: Correctly importing the path module

const CONFIG = {
    mdFolders: [
        'baira_directory/agency_part_1',
        'baira_directory/agency_part_2',
        'baira_directory/agency_part_3',
        'baira_directory/agency_part_4',
        'baira_directory/agency_part_5',
        'baira_directory/agency_part_6',
        'baira_directory/agency_part_7',
        'baira_directory/agency_part_8',
        'baira_directory/agency_part_9',
        'baira_directory/agency_part_10',
        'baira_directory/agency_part_11',
        'baira_directory/agency_part_12',
        'baira_directory/agency_part_13',
        'baira_directory/agency_part_14',
        'baira_directory/agency_part_15',
        'baira_directory/agency_part_16',
        'baira_directory/agency_part_17',
        'baira_directory/agency_part_18',
        'baira_directory/agency_part_19',
        'baira_directory/agency_part_20',
        'baira_directory/agency_part_21',
        'baira_directory/agency_part_22',
        'baira_directory/agency_part_23',
        'baira_directory/agency_part_24',
        'baira_directory/agency_part_25'
    ],
    publicFolders: ['public_1', 'public_2', 'public_3'],
    outputFile: 'agency.json'
};

async function findImage(id) {
    for (const folder of CONFIG.publicFolders) {
        const imgPath = `${folder}/${id}.jpg`;
        try {
            await fs.access(imgPath);
            return imgPath;
        } catch {}
    }
    return "N/A";
}

function parseContent(content) {
    const entry = {};
    const lines = content.split('\n');
    lines.forEach(line => {
        const parts = line.split(':');
        if (parts.length >= 2) {
            const key = parts[0].trim().toLowerCase().replace(/\s+/g, '_');
            const value = parts.slice(1).join(':').trim();
            entry[key] = value;
        }
    });
    return entry;
}

async function start() {
    const allAgencies = [];
    
    for (const folder of CONFIG.mdFolders) {
        try {
            const files = await fs.readdir(folder);
            for (const file of files) {
                if (file.endsWith('.md')) {
                    const content = await fs.readFile(`${folder}/${file}`, 'utf-8');
                    const data = parseContent(content);
                    const id = data.license_no || data.rl_no || data.id || path.parse(file).name;
                    data.photo = await findImage(id);
                    allAgencies.push(data);
                }
            }
        } catch (e) {
            console.error(`Error reading ${folder}:`, e.message);
        }
    }

    await fs.writeFile(CONFIG.outputFile, JSON.stringify(allAgencies, null, 2));
    console.log(`Finished! Total: ${allAgencies.length} agencies.`);
}

start();
