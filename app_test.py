import unittest
import requests

class ApiTest(unittest.TestCase):
    API_URL="http://127.0.0.1:5000/api"
    INFO_URL="{}/info".format(API_URL)
    EDIT_URL="{}/edit".format(API_URL)
    DATA={
                "Description":"Meeting with Rakesh",
                "Date":"2021-08-23",
                "StartTime":"10:00:07",
                "EndTime":"13:00:12",
                "EventCalendar":"false",
                "Status":"To do"
            }
    EXPECTED_RESULT= {
    "Description": "Meeting with MR.X",
    "Date": "2021-08-29",
    "StartTime": "12:00:07",
    "EndTime": "13:00:12",
    "EventCalendar": "false",
    "Status": "To do"
}

    UPDATE_INFO={
    "Description": "Meeting with Rakesh",
    "Date": "2021-08-23",
    "StartTime": "10:00:07",
    "EndTime": "13:00:12",
    "EventCalendar": "false",
    "Status": "Completed"
}

    def test_1_get_all_info(self):
        r=requests.get(ApiTest.INFO_URL)   
        self.assertEqual(len(r.json()),2)
        print("Test 1 completed")

    def test_2_post_info(self):
        resp= requests.post(self.INFO_URL,json=self.DATA)
        self.assertEqual(resp.status_code,200)
        print("Test 2 completed")

    def test_3_get_specific_todo(self):
         resp=requests.get(ApiTest.EDIT_URL+'/1') 
         self.assertEqual(resp.status_code,200)
         self.assertDictEqual(resp.json(),self.EXPECTED_RESULT)
         print("Test 3 completed")

    def test_4_delete(self):
        resp=requests.delete(self.EDIT_URL+'/3')
        self.assertEqual(resp.status_code,200)
        print("Test 4 completed")

    def test_5_update(self):
        resp=requests.put(self.EDIT_URL+'/2',self.UPDATE_INFO)
        self.assertEqual(resp.status_code,200)
        print("Test 5 completed")

if __name__=="__main__":
    tester=ApiTest()
    tester.test_1_get_all_info()
    tester.test_2_post_info()
    tester.test_3_get_specific_todo()
   # tester.test_4_delete() 
    tester.test_5_update()

