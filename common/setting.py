# coding = utf-8

from selenium.webdriver.common.by import By

# 测试用例路径
case_path = "testcase_yaml"

# 配置文件路径
config_path = "config/config.yaml"

# pytest配置文件路径
pytest_ini_path = "config/pytest.ini"

# 日志路径
log_path = "logs/pytest.log"

# 浏览器驱动类型
driver_type = "chrome"

# 最大等待时间
wait_max_time = 10

# 定位方式
selenium_by = By.XPATH

# 定位元素的yaml文件
loc_yaml = "data/loc_yaml/login.yaml"
