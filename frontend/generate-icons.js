const fs = require('fs');
const { createCanvas, loadImage } = require('canvas');

async function generateIcons() {
  const svgContent = fs.readFileSync('./public/icon.svg', 'utf8');

  // Create a data URL from SVG
  const svgDataUrl = `data:image/svg+xml;base64,${Buffer.from(svgContent).toString('base64')}`;

  try {
    const img = await loadImage(svgDataUrl);

    // Generate 192x192 PNG
    const canvas192 = createCanvas(192, 192);
    const ctx192 = canvas192.getContext('2d');
    ctx192.drawImage(img, 0, 0, 192, 192);
    const buffer192 = canvas192.toBuffer('image/png');
    fs.writeFileSync('./public/logo192.png', buffer192);
    console.log('✓ Generated logo192.png');

    // Generate 512x512 PNG
    const canvas512 = createCanvas(512, 512);
    const ctx512 = canvas512.getContext('2d');
    ctx512.drawImage(img, 0, 0, 512, 512);
    const buffer512 = canvas512.toBuffer('image/png');
    fs.writeFileSync('./public/logo512.png', buffer512);
    console.log('✓ Generated logo512.png');

    // Generate favicon (32x32)
    const canvas32 = createCanvas(32, 32);
    const ctx32 = canvas32.getContext('2d');
    ctx32.drawImage(img, 0, 0, 32, 32);
    const buffer32 = canvas32.toBuffer('image/png');
    fs.writeFileSync('./public/favicon.ico', buffer32);
    console.log('✓ Generated favicon.ico');

    console.log('\n✅ All icons generated successfully!');
  } catch (error) {
    console.error('Error generating icons:', error);
    process.exit(1);
  }
}

generateIcons();
