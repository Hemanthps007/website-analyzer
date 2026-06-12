const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    let urlInput = (req.query.url || '').trim().toLowerCase();
    if (urlInput.endsWith('/')) {
      urlInput = urlInput.slice(0, -1);
    }

    let filePath = path.join(process.cwd(), 'dataset.csv');
    if (!fs.existsSync(filePath)) {
      filePath = path.join(__dirname, '..', 'dataset.csv');
    }
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const lines = fileContent.split(/\r?\n/);
    
    const dataset = {};
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;
      const values = line.split(',');
      if (values.length < 10) continue;
      const csvUrl = values[0].trim().toLowerCase();
      dataset[csvUrl] = {
        visual_design: parseFloat(values[1]),
        mobile_experience: parseFloat(values[2]),
        content_clarity: parseFloat(values[3]),
        accessibility: parseFloat(values[4]),
        navigation: parseFloat(values[5]),
        content_volume: parseFloat(values[6]),
        issues_identified: parseInt(values[7]),
        critical_fixes: parseInt(values[8]),
        score_gain: parseInt(values[9])
      };
    }

    let result;
    if (dataset[urlInput]) {
      result = { ...dataset[urlInput], is_mock: false };
    } else {
      // Generate realistic random data if URL not found
      const randomRange = (min, max) => Math.round((Math.random() * (max - min) + min) * 10) / 10;
      const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
      
      result = {
        visual_design: randomRange(2.0, 9.0),
        mobile_experience: randomRange(2.0, 9.0),
        content_clarity: randomRange(2.0, 9.0),
        accessibility: randomRange(2.0, 9.0),
        navigation: randomRange(2.0, 9.0),
        content_volume: randomRange(2.0, 9.0),
        issues_identified: randomInt(5, 35),
        critical_fixes: randomInt(1, 12),
        score_gain: randomInt(10, 85),
        is_mock: true
      };
    }

    res.status(200).json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
