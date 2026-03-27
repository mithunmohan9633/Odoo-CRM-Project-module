package utils;

import base.BaseTest;
import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.Status;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;

public class TestListener implements ITestListener {
    private static ExtentReports extent = ExtentManager.getInstance();
    private static ThreadLocal<ExtentTest> test = new ThreadLocal<>();
    private static final Logger logger = LogManager.getLogger(TestListener.class);

    @Override
    public void onTestStart(ITestResult result) {
        String testName = result.getMethod().getMethodName();
        String description = result.getMethod().getDescription() != null ? result.getMethod().getDescription() : "";
        Object[] parameters = result.getParameters();

        // If the test uses a DataProvider, append the scenario description (the last parameter)
        if (parameters != null && parameters.length > 0) {
            String scenarioDesc = String.valueOf(parameters[parameters.length - 1]);
            testName = testName + " - " + scenarioDesc;
            description = description + " | Scenario: " + scenarioDesc;
        }

        logger.info("Starting Test: " + testName);
        ExtentTest extentTest = extent.createTest(testName, description);
        test.set(extentTest);
    }

    @Override
    public void onTestSuccess(ITestResult result) {
        logger.info("Test Passed: " + result.getMethod().getMethodName());
        test.get().log(Status.PASS, "Test Executed Successfully");
    }

    @Override
    public void onTestFailure(ITestResult result) {
        logger.error("Test Failed: " + result.getMethod().getMethodName());
        test.get().log(Status.FAIL, "Test Failed: " + result.getThrowable().getMessage());
        
        WebDriver driver = BaseTest.getDriver();
        if (driver != null) {
            logger.info("Capturing screenshot for failed test...");
            try {
                String base64Screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BASE64);
                test.get().addScreenCaptureFromBase64String(base64Screenshot, "Failure Screenshot");
            } catch (Exception e) {
                logger.error("Failed to capture screenshot", e);
            }
        }
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        logger.warn("Test Skipped: " + result.getMethod().getMethodName());
        test.get().log(Status.SKIP, "Test Execution Skipped");
    }

    @Override
    public void onFinish(ITestContext context) {
        logger.info("Test Suite Execution Finished. Flushing Extent Report...");
        extent.flush();
    }
}
