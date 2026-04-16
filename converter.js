const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
    // We only need the parent folder now
    sourceDir: 'baira_directory',
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
    
    try {
        // Read all files directly inside baira_directory
        const files = await fs.readdir(CONFIG.sourceDir);
        
        for (const file of files) {
            if (file.endsWith('.md')) {
                const filePath = path.join(CONFIG.sourceDir, file);
                const content = await fs.readFile(filePath, 'utf-8');
                
                const data = parseContent(content);
                // Fallback to filename if no ID found in content
                const id = data.license_no || data.rl_no || data.id || path.parse(file).name;
                
                data.photo = await findImage(id);
                allAgencies.push(data);
            }
        }
    } catch (e) {
        console.error(`Error processing directory:`, e.message);
    }

    await fs.writeFile(CONFIG.outputFile, JSON.stringify(allAgencies, null, 2));
    console.log(`Finished! Total: ${allAgencies.length} agencies found in ${CONFIG.sourceDir}.`);
}

start();
