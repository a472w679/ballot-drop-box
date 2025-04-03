// reset-modules.ts
import * as fs from 'fs';
import * as path from 'path';

// List of directories to process
const directories = [
  'src/components/Dashboard',
  'src/components/Layout',
  'src/components/Map',
  'src/pages',
  'src/services',
  'src/store',
  'src/store/slices',
  'src/types'
];

// Process each directory
directories.forEach(dir => {
  const directoryPath = path.join(process.cwd(), dir);
  
  try {
    // Read all files in the directory
    const files = fs.readdirSync(directoryPath);
    
    // Process each .ts or .tsx file
    files.forEach(file => {
      if (file.endsWith('.ts') || file.endsWith('.tsx')) {
        const filePath = path.join(directoryPath, file);
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Check if it already has an export statement
        if (!content.includes('export ')) {
          // Add an empty export at the end
          content += '\n\nexport {};\n';
          fs.writeFileSync(filePath, content, 'utf8');
          console.log(`Added export to ${filePath}`);
        }
      }
    });
  } catch (error) {
    console.error(`Error processing directory ${dir}:`, error);
  }
});

console.log('Done processing files.');