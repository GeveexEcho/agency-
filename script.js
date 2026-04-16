const fs = require("fs");
const path = require("path");

// folders
const MD_DIR = "./baira_directory";
const IMAGE_DIRS = ["./public_1", "./public_2", "./public_3"];

// store all images
const imageMap = {};

// 🔍 Step 1: Read all images and map RL number
IMAGE_DIRS.forEach(dir => {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const match = file.match(/RL_(\d+)\.jpg/i);
        if (match) {
            const rl = match[1];
            imageMap[rl] = `${dir}/${file}`;
        }
    });
});

console.log("Total Images Found:", Object.keys(imageMap).length);

// 📄 Step 2: Read all markdown files
const allData = [];

for (let i = 1; i <= 25; i++) {
    const filePath = path.join(MD_DIR, `agency_part_${i}.md`);
    const content = fs.readFileSync(filePath, "utf-8");

    const lines = content.split("\n");

    lines.forEach(line => {
        if (!line.startsWith("|") || line.includes("SL No.")) return;

        const cols = line.split("|").map(c => c.trim());

        if (cols.length < 7) return;

        const agencyInfo = cols[2]; // Agency Name & RL
        const photo = cols[4];

        // extract RL number
        const rlMatch = agencyInfo.match(/RL No:\s*(\d+)/i);
        const rl = rlMatch ? rlMatch[1] : null;

        let photoPath = "N/A";

        if (rl && imageMap[rl]) {
            photoPath = imageMap[rl];
        }

        const obj = {
            sl: cols[1],
            agency: agencyInfo,
            owner: cols[3],
            photo: photoPath,
            address: cols[5],
            contact: cols[6],
            email: cols[7] || ""
        };

        allData.push(obj);
    });
}

console.log("Total Agencies:", allData.length);

// 💾 Step 3: Save JSON
fs.writeFileSync("agency.json", JSON.stringify(allData, null, 2));

console.log("✅ agency.json generated!");
