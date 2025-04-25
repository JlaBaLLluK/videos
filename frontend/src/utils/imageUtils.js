export async function getFileFromUrl(imageUrl) {
  console.log(imageUrl);
  const response = await fetch(imageUrl);
  const fileName = response.url.split('/').pop();
  const blob = await response.blob();
  return new File([blob], fileName, { type: blob.type });
}
