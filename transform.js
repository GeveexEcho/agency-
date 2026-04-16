const fs = require('fs');

// ✅ তোমার file name এখানে
const rawData = fs.readFileSync('agency.json', 'utf-8');
const data = JSON.parse(rawData);

const updatedData = data.map(item => {
    let agencyName = item.agency;
    let rlNo = '';

    // RL No extract
    const match = agencyName.match(/RL No:\s*\d+/i);

    if (match) {
        rlNo = match[0]; // "RL No: 1857"
        agencyName = agencyName.replace(match[0], '').trim();
    }

    return {
        ...item,
        agency: agencyName,
        rlNo: rlNo
    };
});

// ✅ new file তৈরি হবে
fs.writeFileSync('updated-agency.json', JSON.stringify(updatedData, null, 2));

console.log('✅ Done! File saved as updated-agency.json');
