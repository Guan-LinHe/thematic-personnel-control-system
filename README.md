![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/Welcome%20window.jpg)
# 人員管制系統 thematic personnel control system
<h>The idea of the personnel control system comes from daily life. There are a large number of people entering and leaving the company or the community. From observations, it is found that the security or management personnel cannot confirm the identity of the personnel, resulting in unsafe access control. Although some companies now use gates or Control system, but due to the limited funds of the company or building, in order to achieve low-cost development to ensure the safety of personnel in and out, and to achieve low-cost and low-capacity management, I thought about this system. This system uses Python programs. Language development, and use the Tkinter module as the GUI window to facilitate the management of the administrator, use the video camera and the Opencv module and the Dlib face training model (Davis King-2014) to achieve the face recognition of the recognizer, and combine it Check-in and query personnel entry and exit and count the number of people system, use account login to distinguish administrator rights, and add the photo of the recognizer and the photo taken by the video to compare the matrix to capture the smallest photo name and display the file name of the recognized photo It is the name. The accuracy of face recognition is 99.38% through experimental test data and data from Dlib's official website.</h>
# 系統架構方塊圖 System architecture block diagram
![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/flow%20chart.png)
# 功能演示 Demo
<h>The personnel control system can be divided into system administrators and group administrators. When entering the login screen, you can choose account login or face recognition method to log in. After logging in, the system administrator can manage all account follow-up information, and the group administrator can only open it Video recognition and view recognition names and group manager accounts are added.</h>
<dl>
  <dt>Welcome window</dt>
  
  * Execution screen
  <dd>Run the program and there will be a welcome window, and click to enter the function.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/Welcome%20window.jpg)
  
  * System introduction
  
  <dd>When you click on the system introduction, it will jump to the system introduction window, with the developer's information and function description.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/System%20introduction%20window.png)
  
  <dt>Login window</dt>
  
  * Login with account password
   
   ```
  #System administrator
  account number:admin
  password:123
  #Group manager
  account number:group
  password:123
  ```
  <dd>Use the account password to log in, identify the user as a system administrator or group administrator, and automatically pop up the selection window.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/Login%20window.png)
  
  * Face login
  
  <dd>Use the camera to take a photo of the face and recognize it to confirm the identity of the system administrator or group administrator, and automatically pop out of the menu window.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/Face%20login%20window.jpg)
  
  
  <dt>System administrator function</dt>
   
  <h>The system administrator account is the highest authority, which can add and view accounts and other administrative authority.</h>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/System%20administrator%20function%20menu.png)

   * Added all staff menu
  
  <dd>With this function, you can add system administrator accounts and group administrator accounts, and you can choose the file mode to add new photos or take photos immediately, and you can modify and delete the photos and account contents.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/Account%20management%20for%20all%20personnel.PNG)
  
  * Personnel identification management menu
  
  <dd>This function can manage personnel entering and exiting, video identification whether there is a person or employee, to achieve access control management, use new photos or immediately take photos to add new personnel, and can view and delete photos.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/Personnel%20access%20identification%20addition%20and%20management.png)
  
   * Recognizers view the menu
  
  <dd>This function checks the name, age, gender, number of times of entry and exit of the personnel recognized by the video, and clicks on the personnel, and the photo of the personnel account added by the system administrator and the photo of the personnel recognized by the video will be displayed.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/5272c4c475b8283b5f5a860341cae32dec765efd/Github%20picture/Identifier%20information%20view.png)
  
  * In and out statistics view menu
  
  <dd>This function can check the total number of people entering and exiting, the number of boys, the number of girls, and the number of strangers counted today and other times, and it can also clear the chart.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/4c029af309a3e890b27adfaba4daad67c6f552b6/Github%20picture/Access%20statistics%20view.png)
  
   <dt>Group manager function</dt>
   
  <h>The group administrator account has only specific permissions, which can enable management permissions such as personnel identification and specific account addition.</h>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/4c029af309a3e890b27adfaba4daad67c6f552b6/Github%20picture/Group%20manager%20function%20menu.png)
  
  * Personnel identification menu
  
  <dd>This function is to use the camera to turn on and identify the identity of the person entering and leaving. If there is a picture of the person, the name, age, male and female (boys are blue, girls are pink), and there is a green frame, if there is no such person It will display Unknow, age, gender (blue for boys and pink for girls), a red box warning and email warning, and all the displayed data will be written into the Pickle database.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/4c029af309a3e890b27adfaba4daad67c6f552b6/Github%20picture/Personnel%20identification%20correct%20and%20wrong%20and%20Email%20warning.PNG)
  
  
   * View the recognition menu
  
  <dd>This function can view the name, date, size, and time of the last update of the identification person, and allows the door staff to check whether there is the person's name, but not the photo. The identification may cause information security risks.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/4c029af309a3e890b27adfaba4daad67c6f552b6/Github%20picture/View%20identification%20personnel%20information.png)
  
   * Add group personnel menu
  
  <dd>This function can only add group administrators and cannot add administrator accounts to reach the authority management. First add account group administrators and then choose computer file method to add photos or immediately take photos to add photos, which can be viewed in The function to view and delete account and photo content in Photos and Account Contents.</dd>
  
  ![image](https://github.com/GuanLinHu/thematic-personnel-control-system/blob/4c029af309a3e890b27adfaba4daad67c6f552b6/Github%20picture/Add%20group%20account%20function.png)
  
  # 感謝 grateful
   >December 28, 2020 Yadong Institute of Technology(Present[Asia Eastern University of Science and Technology](https://www.aeust.edu.tw/)For the special exhibition, thank you instructor Professor Jiong San for his teaching and Jin Jie and Guan Lin's collaboration to complete this special topic.
   
   >The [Dayeh University](https://www.dyu.edu.tw/) Department of Asset Management will hold the 22nd Session of Electronic Enterprise Management Theory and Practice Seminar in 2021, which is included in the paper.
  </dl>
