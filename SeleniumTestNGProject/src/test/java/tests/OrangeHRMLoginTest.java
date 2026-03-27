package tests;

import base.BaseTest;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import pages.OrangeHRMLoginPage;
import utils.ConfigReader;

import java.awt.Desktop;
import java.io.File;
import java.io.IOException;
import org.testng.annotations.AfterSuite;

public class OrangeHRMLoginTest extends BaseTest {
    private static final Logger logger = LogManager.getLogger(OrangeHRMLoginTest.class);

    @Test(priority = 1, description = "Verifies successful login with valid credentials")
    public void testValidLogin() {
        logger.info("Starting valid login scenario...");
        OrangeHRMLoginPage loginPage = new OrangeHRMLoginPage(getDriver());
        loginPage.login(ConfigReader.getProperty("username"), ConfigReader.getProperty("password"));
        Assert.assertTrue(loginPage.isDashboardDisplayed(), "Dashboard is not displayed after valid login.");
    }

    @Test(priority = 2, dataProvider = "invalidLoginData", description = "Verifies login failures using Data Provider")
    public void testInvalidLoginScenarios(String username, String password, String expectedError, String scenarioDesc) {
        logger.info("Executing invalid login scenario: " + scenarioDesc);
        OrangeHRMLoginPage loginPage = new OrangeHRMLoginPage(getDriver());
        loginPage.login(username, password);
        
        if (!expectedError.isEmpty()) {
            Assert.assertEquals(loginPage.getErrorMessage(), expectedError, "Error message mismatch for scenario: " + scenarioDesc);
        } else {
            Assert.assertTrue(getDriver().getCurrentUrl().contains("login"), "Should remain on login page for empty credentials.");
            logger.info("Empty credentials correctly prevented login.");
        }
    }

    @DataProvider(name = "invalidLoginData")
    public Object[][] getInvalidLoginData() {
        return new Object[][] {
            { ConfigReader.getProperty("username"), "wrongpassword", "Invalid credentials", "Valid User, Invalid Pass" },
            { "WrongUser", ConfigReader.getProperty("password"), "Invalid credentials", "Invalid User, Valid Pass" },
            { "WrongUser", "wrongpassword", "Invalid credentials", "Invalid User, Invalid Pass" },
            { "", "", "", "Empty Credentials" }
        };
    }

    @AfterSuite
    public void openReport() {
        try {
            File htmlReport = new File("target/ExtentReport.html");
            if (htmlReport.exists()) {
                logger.info("Auto-opening Extent HTML Report format...");
                Desktop.getDesktop().browse(htmlReport.toURI());
            }
        } catch (IOException e) {
            logger.error("Could not automatically open HTML report.", e);
        }
    }
}
