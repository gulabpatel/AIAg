// importAll: Dynamically imports all modules (e.g., images) from a given context (directory).
// It returns an object where keys are file names and values are the imported modules.
function importAll(r) {
  let images = {};
  r.keys().forEach((item, index) => {
    images[item.replace('./', '')] = r(item);
  });
  return images;
}

// weatherIcon: Returns the specific weather icon image based on the provided image name.
// It uses dynamic imports to load all weather icons from a specific directory.
export function weatherIcon(imageName) {
  const allWeatherIcons = importAll(
    require.context('../assets/icons', false, /\.(png)$/)
  );

  const iconsKeys = Object.keys(allWeatherIcons);

  const iconsValues = Object.values(allWeatherIcons);
  const iconIndex = iconsKeys.indexOf(imageName);

  return iconsValues[iconIndex];
}
