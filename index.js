const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');  // Fixed 'required' to 'require'

async function searchGoogle() {
  // Create a new instance of the Chrome WebDriver
  const driver = await new Builder()
    .forBrowser('chrome')  // Specify browser as 'chrome'
    .setChromeOptions(new chrome.Options())  // Set Chrome options
    .build();
  
  try {
    // Navigate to Google
    await driver.get('https://www.google.com');

    // Find the search input field using its name attribute
    const searchBox = await driver.findElement(By.name('q'));

    // Type the search query into the search box
    await searchBox.sendKeys('Selenium WebDriver', Key.RETURN);  // Key.RETURN simulates pressing Enter
    
    // Wait until the results page is loaded and title contains 'Selenium WebDriver'
    await driver.wait(until.titleContains('Selenium WebDriver'), 10000);

    console.log('Search completed!');

  } finally {
    // Close the browser after the operation
    await driver.quit();
  }
}

// Execute the searchGoogle function
searchGoogle();
