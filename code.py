import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
filename1 = 'king_Rahul.xlsx'
filename2 = 'land_bisaal.xlsx'

Sheet1 = pd.read_excel(filename1).to_dict()
Sheet2 = pd.read_excel(filename2)

Sheet1dict = {}
length = len(Sheet1['tracking_id'])
for index in range(length):
    Sheet1dict[Sheet1['tracking_id'][index]]=datetime.strptime(Sheet1['dispatch_date'][index], "%d-%m-%Y %I:%M%p")

tracking_sheet2 = {}

# Loop through each row in the DataFrame
for index, row in Sheet2.iterrows():
    # Get the tracking ID and in_scan_time values for the current row
    tracking_id = row['vendor_tracking_id']
    in_scan_time = row['inscan_time']
    value = row['bag_tracking_id']
    # If the tracking ID is not already in the dictionary, add it with an empty list
    if tracking_id not in tracking_sheet2:
        tracking_sheet2[tracking_id] = []

    # Append the in_scan_time value to the list for the current tracking ID
    tracking_sheet2[tracking_id].append({"value": value, "time":in_scan_time})

Primary_breach_count = 0

Secondary_breach_count = 0

Bag_closing_breach_count = 0

connected_count = 0
final_array = []
# Iterate through the dictionary using a for loop
for key, value in Sheet1dict.items():
    if(key in tracking_sheet2):

        inscan_time_1 = None
        inscan_time_2 = None
        inscan_time_3=None
        last_null_time = None
        for ele in tracking_sheet2[key]:
            
            if( ele['value']== 'null'):
                if( inscan_time_1 == None ):
                    inscan_time_1 = ele['time']
                else:
                    last_null_time = ele['time']
            elif (inscan_time_3 == None):
                inscan_time_3 = ele['time']
        status = None
        
        if(inscan_time_1 and value and int((inscan_time_1-value).total_seconds() / 60) > 50 ):
            status = "Primary Breach"
            Primary_breach_count+=1
        elif(  inscan_time_1 and inscan_time_2 and int((inscan_time_2-inscan_time_1).total_seconds() / 60) > 30):
            status= "Secondary Breach"
            Secondary_breach_count+=1
        elif(inscan_time_2 and inscan_time_3 and int((inscan_time_3-inscan_time_2).total_seconds() / 60) > 30) :
            status= "Bag Closing Breach"
            Bag_closing_breach_count+=1
        else :
            status = "Connnected" 
            connected_count+=1
        if(value):
            value = value.strftime('%Y-%m-%d %H:%M:%S')      
        if(inscan_time_1):
            inscan_time_1  = inscan_time_1.strftime('%Y-%m-%d %H:%M:%S')    
        if(inscan_time_2):
            inscan_time_2  = inscan_time_2.strftime('%Y-%m-%d %H:%M:%S')
        if(inscan_time_3):
            inscan_time_3  = inscan_time_3.strftime('%Y-%m-%d %H:%M:%S')                           
        final_array.append({"Tracking_Id" : key , "Dispatch date": value, "First scan time" : inscan_time_1, "Second scan time" : inscan_time_2, "Third Scan Time": inscan_time_3, "Status": status}) 
        

df = pd.DataFrame(final_array)       
print("Primary_breach_count  ", Primary_breach_count)
print("Secondary_breach_count ", Secondary_breach_count)
print("Bag_closing_breach_count ",Bag_closing_breach_count)
print("connected_count ",connected_count)                    

            
df.to_excel('outptrdfeut.xlsx', index=False)