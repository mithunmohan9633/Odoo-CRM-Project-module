package pages;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class OrangeHRMLoginPage {
    private WebDriver driver;
    private WebDriverWait wait;
    private static final Logger logger = LogManager.getLogger(OrangeHRMLoginPage.class);

    // PageFactory Elements
    @FindBy(name = "username")
    private WebElement usernameInput;

    @FindBy(name = "password")
    private WebElement passwordInput;

    @FindBy(css = "button[type='submit']")
    private WebElement loginButton;

    @FindBy(css = ".oxd-alert-content-text")
    private WebElement errorMessage;

    @FindBy(css = ".oxd-topbar-header-breadcrumb h6")
    private WebElement dashboardHeader;

    public OrangeHRMLoginPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);
    }

    public void login(String username, String password) {
        logger.info("Attempting login with username: [" + username + "] and password: [" + password + "]");
        wait.until(ExpectedConditions.visibilityOf(usernameInput)).sendKeys(username);
        passwordInput.sendKeys(password);
        loginButton.click();
    }

    public String getErrorMessage() {
        String errorMsg = wait.until(ExpectedConditions.visibilityOf(errorMessage)).getText();
        logger.info("Validation Error Message displayed: " + errorMsg);
        return errorMsg;
    }

    public boolean isDashboardDisplayed() {
        try {
            boolean isDisplayed = wait.until(ExpectedConditions.visibilityOf(dashboardHeader)).isDisplayed();
            logger.info("Successfully landed on Dashboard view.");
            return isDisplayed;
        } catch (Exception e) {
            logger.error("Dashboard validation failed, element not visible.");
            return false;
        }
    }
}
