package base;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import utils.ConfigReader;

import java.time.Duration;

public class BaseTest {
    private static ThreadLocal<WebDriver> driver = new ThreadLocal<>();
    private static final Logger logger = LogManager.getLogger(BaseTest.class);

    public static WebDriver getDriver() {
        return driver.get();
    }

    @BeforeMethod
    public void setUp() {
        String browser = ConfigReader.getProperty("browser");
        logger.info("Setting up WebDriver for browser: " + browser);
        WebDriver tempDriver = null;
        if (browser.equalsIgnoreCase("chrome")) {
            WebDriverManager.chromedriver().setup();
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--remote-allow-origins=*");
            tempDriver = new ChromeDriver(options);
        } else if (browser.equalsIgnoreCase("firefox")) {
            WebDriverManager.firefoxdriver().setup();
            tempDriver = new FirefoxDriver();
        }
        
        if (tempDriver != null) {
            tempDriver.manage().window().maximize();
            tempDriver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
            tempDriver.get(ConfigReader.getProperty("url"));
            driver.set(tempDriver);
            logger.info("WebDriver initialized and navigated to URL successfully.");
        } else {
            logger.error("Failed to initialize WebDriver.");
        }
    }

    @AfterMethod
    public void tearDown() {
        if (getDriver() != null) {
            logger.info("Tearing down WebDriver instance.");
            getDriver().quit();
            driver.remove();
        }
    }
}
