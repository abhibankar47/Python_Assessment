How To Run the Code
1. Open the Folder Abhinandan Codes in VS Code
2. Open util.py test_util.py in separate tab. The example.log file contains all the data related to your project which it will get fetched when you run util.py file along with commands you enter(which are in point 4)
3. run each of them in the vs code terminal
4. following commands should be entered , individually
  python util.py -h
  python util.py --first 10 example.log
  python util.py --last 5 example.log
  python util.py --timestamps example.log
  python util.py --ipv4 example.log
  python util.py --ipv6 example.log
  python util.py --last 50 --ipv4 example.log
  For multiple options used at once we run the code (intersection of two inputs)
  python util.py --first 20 --ipv4  example.log 
5. Now you can run the test_util.py file for test case using the command below (make sure both util.py and test_util.py file are open in vs code)
   python -m unittest test_util.py
