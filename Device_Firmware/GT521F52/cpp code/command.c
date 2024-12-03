#include "definition.h"
#include "stdio.h"
#include "stdlib.h"  
#include "wiringPi.h"
#include "wiringSerial.h"

int serial_var; //for raspberry UART handle

FILE *pFile;  //for handle file

void SendCommand(unsigned char *ucData,unsigned int length)
{
   unsigned int i;
   for(i = 0; i < length; i++)
      serialPutchar(serial_var,*(ucData + i));
}

void ReceiveCommand(unsigned char *ucData,unsigned int length)
{
   unsigned int i=0,time_out=0;
   
   do
    {
     if(serialDataAvail(serial_var)>0)  //check RX buffer
       {
       if(i < length)
       	{
         *(ucData + i) = serialGetchar(serial_var);
         i++;         
        }
       }
     else
       {
       delay(10);
       time_out++;
       if(time_out==300)
         {
          printf("No fingerprint module\n");
          exit(0);  
         }
       }
    }while(i<length);  //check total package length
}

unsigned short CalcChkSumOfCmdAckPkt(COMMAND_PACKAGE_STRUCTURE *pPkt)
{
   unsigned short wChkSum = 0;
   unsigned char *pBuf = (unsigned char*)pPkt;
   int i;
	
   for(i=0;i<(sizeof(COMMAND_PACKAGE_STRUCTURE)-2);i++)
      wChkSum += pBuf[i];

   return wChkSum;
}

unsigned short CalcChkSumOfDataPkt(DATA_PACKAGE_STRUCTURE *pPkt)
{
   unsigned short wChkSum = 0;
   unsigned char *pBuf = (unsigned char*)pPkt;
   int i;
	
   for(i=0;i<(sizeof(DATA_PACKAGE_STRUCTURE)-2);i++)
      wChkSum += pBuf[i];

   return wChkSum;
}

void send_receive_command()
{
   SendCommand(&command_package.Head1,COMMAND_PACKAGE_LENGTH);
   ReceiveCommand(&command_package.Head1,COMMAND_PACKAGE_LENGTH);  
  
   return_para=command_package.nParam;
   return_ack=command_package.wCmd;
}

void FP_Open()
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000000;
  command_package.wCmd=OPEN;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();
}

void FP_LED_open()
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000001; 
  command_package.wCmd=CMOSLED;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();
}

void FP_LED_close()
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000000; 
  command_package.wCmd=CMOSLED;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();
}

void FP_GetEnrollCount()
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000000; 
  command_package.wCmd=GETENROLLCOUNT;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();
}

void FP_EnrollStart(int specify_ID)
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=specify_ID; 
  command_package.wCmd=ENROLLSTART;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command(); 
}  

void FP_Enroll(int Enroll_define)
{
  unsigned short Enroll_command;
  
  switch(Enroll_define)
    {
      case 1:
             Enroll_command=ENROLL1;
             break;
      case 2:
             Enroll_command=ENROLL2;
             break;
      case 3:
             Enroll_command=ENROLL3;
             break;      
    }
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000000;
  command_package.wCmd=Enroll_command;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command(); 
}

void FP_IsPressFinger()
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000000; 
  command_package.wCmd=ISPRESSFINGER;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();  
} 

void FP_CaptureFinger(unsigned long picture_quality)
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=picture_quality; 
  command_package.wCmd=CAPTURE_FINGER;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();  
}

void FP_DeleteAll()
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000000; 
  command_package.wCmd=DELETEALL;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();
}

void FP_Identify()
{
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000000; 
  command_package.wCmd=IDENTIFY;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();
}

void FP_GetTemplate(int specify_ID)
{
	
  char filename[64];  
  sprintf(filename,"%d-template.bin",specify_ID);
	
	command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=specify_ID; 
  command_package.wCmd=GETTEMPLATE;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
	send_receive_command();
	
	if(return_ack!=ACK)
		{
		 printf("NO template for current ID!\n");
	   return;
	  }

	ReceiveCommand(&data_package.Head1,DATA_PACKAGE_LENGTH);   //read template to receive buffer from fingeprint module
  
  pFile = fopen(filename,"w");    
  if( NULL == pFile )
   	{
     printf("open failure");
     return;
    }
  else
   	fwrite(data_package.nData,1,sizeof(data_package.nData),pFile);  
  
  fclose(pFile);
  printf("Created %d-template.bin on this folder!\n",specify_ID);  
}

void FP_SetTemplate(int specify_ID)
{
	char template_name[64];
	
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=specify_ID; 
  command_package.wCmd=SETTEMPLATE;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  	
	send_receive_command();
	if(return_ack!=ACK)
		{
		 printf("Occipied for current ID!\n");
	   return;
	  }
	
	printf("please input template name:\n");
	scanf("%s",&template_name);	
	
  pFile = fopen(template_name,"r");
  if( NULL == pFile )
   	{
     printf("open failure, please create template file by GetTemplate");
     return;
    }
  else
   	fread(data_package.nData,1,sizeof(data_package.nData),pFile);  
  
  fclose(pFile);

  data_package.Head1=DATA_START_CODE1;  		  
  data_package.Head2=DATA_START_CODE2;
  data_package.wDevId=DEVICE_ID;
  data_package.wChkSum=CalcChkSumOfDataPkt(&data_package);
	
  SendCommand(&data_package.Head1,DATA_PACKAGE_LENGTH);
  ReceiveCommand(&command_package.Head1,COMMAND_PACKAGE_LENGTH);  
   
  return_para=command_package.nParam;
  return_ack=command_package.wCmd; 

  if(return_ack==ACK)
  	 printf("ID=%d SetTempalte successful!\n",specify_ID); 
  else
  	 printf("Template file is duplicatd with fingerprint module content, SetTemplate fail!\n");	 
}

void FP_GetDatabase()
{
  unsigned int specify_ID,loop_time;	 
	
  pFile = fopen("FP_database.bin","w+");
  if(NULL == pFile)
  	{
  	printf("open file failure!\n");
  	return;
  	}
	
	for(specify_ID=0;specify_ID<FP_MAX_SIZE;specify_ID++)   
	   {
	   	printf("Getting ID=%d template!\n",specify_ID);  
	   	
		command_package.Head1=COMMAND_START_CODE1;  
  		command_package.Head2=COMMAND_START_CODE2;
  		command_package.wDevId=DEVICE_ID;
  		command_package.nParam=specify_ID; 
  		command_package.wCmd=GETTEMPLATE;
  		command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  		
		send_receive_command();	
	    
	    if(return_ack != ACK)
		    {      
		     for(loop_time=0;loop_time<498;loop_time++)		    
	          data_package.nData[loop_time]=0x00;	      
	        }
	    else	    	   
			ReceiveCommand(&data_package.Head1,DATA_PACKAGE_LENGTH);

   		fwrite(data_package.nData,1,sizeof(data_package.nData),pFile);    			
   	 }
  fclose(pFile);  	
  printf("Created FP_database.bin on this folder!\n");  
}

void FP_SetDatabase()
{
  unsigned int specify_ID,loop_time;
  unsigned char ignore_template[498];
  char occipied_ID[FP_MAX_SIZE];
  //read file  
  pFile = fopen("FP_database.bin","r");
  if( NULL == pFile )
   	{
     printf("open failure, please make sure FP_database.bin exist!\n");
     return;
    }
    
  for(loop_time=0;loop_time<FP_MAX_SIZE;loop_time++)   
      occipied_ID[loop_time]=-1;
  loop_time=0;
  
	for(specify_ID=0;specify_ID<FP_MAX_SIZE;specify_ID++)
	   {
	   	printf("Setting ID=%d template!\n",specify_ID);   
	
	  command_package.Head1=COMMAND_START_CODE1;  
      command_package.Head2=COMMAND_START_CODE2;
      command_package.wDevId=DEVICE_ID;
      command_package.nParam=specify_ID; 
      command_package.wCmd=SETTEMPLATE;
      command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  	
	    send_receive_command();
	    if(return_ack!=ACK)  
	    	{	    		
	    	 occipied_ID[loop_time]=specify_ID;    
	    	 loop_time++;
	    	 fread(ignore_template,1,sizeof(data_package.nData),pFile); 
	    	}
	    else
	    	{
	      fread(data_package.nData,1,sizeof(data_package.nData),pFile);       	
	      
	    data_package.Head1=DATA_START_CODE1;  
        data_package.Head2=DATA_START_CODE2;
        data_package.wDevId=DEVICE_ID;
	    data_package.wChkSum=CalcChkSumOfDataPkt(&data_package);
	      
        SendCommand(&data_package.Head1,DATA_PACKAGE_LENGTH);
        ReceiveCommand(&command_package.Head1,COMMAND_PACKAGE_LENGTH);
         
        return_para=command_package.nParam;
        return_ack=command_package.wCmd;         
        }
     }
     fclose(pFile); 	 

     printf("Duplicated ID(No SetTemplate) as below:\n");
     for(loop_time=0;loop_time<200;loop_time++) 
       {
       	if(occipied_ID[loop_time]!=255)
          printf("ID=%d\n",occipied_ID[loop_time]);
       }
       
     printf("Finish of FP_database.bin to fingerprint module!\n");    
}

void FP_DeviceSerialNumber()
{
  unsigned char get_data[28],serial_number[20];
	
  command_package.Head1=COMMAND_START_CODE1;  
  command_package.Head2=COMMAND_START_CODE2;
  command_package.wDevId=DEVICE_ID;
  command_package.nParam=0x00000001; 
  command_package.wCmd=OPEN;
  command_package.wChkSum=CalcChkSumOfCmdAckPkt(&command_package);
  
  send_receive_command();

  unsigned int i=0,time_out=0;
   
   do
    {
     if(serialDataAvail(serial_var)>0)  //check RX buffer
       {
       if(i < 30)   
       	{
         get_data[i]= serialGetchar(serial_var);
         i++;         
        }
       }
     else
       {
       delay(100);
       time_out++;
       if(time_out==30)
         {
          printf("No fingerprint module!\n");
          exit(0);  
         }
       }
    }while(i<30);  //check total package length  
   
  for(i=12;i<=27;i++)      //show serial number
    printf("%x",get_data[i]); 	
  printf("\n");  
    
}
