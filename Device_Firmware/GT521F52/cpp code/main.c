#include "definition.h"
#include "command.h"
#include "stdio.h"  
#include "stdlib.h" 
#include "wiringPi.h" //load WiringPi library
#include "wiringSerial.h"  //load WiringPi serial library

int serial_var;    

int main() 
{	
   unsigned int menu_loop=1,choose_function;  //for menu handle
   unsigned int loop_time; 	 
	 
   if (wiringPiSetup () == -1 ) exit (1);  //for wiringPi GPIO 
	
   pinMode(TOUCH_PIN, INPUT) ;    //Setting direction of pin
	 
   //check UART coummunication about WiringPi library,Raspberry and Fingerprint
   if(wiringPiSetup() < 0)
	 {
	  printf("WiringPi-UART error!");
	  return -1;
     }
    
   if((serial_var = serialOpen("/dev/ttyAMA0",9600)) < 0)
   	 {
   	 printf("Raspberry-UART error!");
   	 return -1;
	 }
	   
   FP_Open(); 
   if(return_ack == NACK)  
   	 {
   	 printf("Fingerprint-UART error...\n");
   	 return -1;   
     }
   
   //main functions
   while(menu_loop==1)
    {   	
    printf("------------------------------------\n");     
    printf("**Fingprinter module demo**\n");
    #if (FP_TOUCH ==1) 
	   printf("<Touch function is enable>\n");
    #else
       printf("<Touch function is disable>\n");
    #endif
    printf("Please choose functions:\n");
    printf("|1.Enrollment\n");
    printf("|2.Identify\n");
    printf("|3.Delete All\n");
    printf("|4.Get User Count\n");
    printf("|5.Get Template\n");
    printf("|6.Set Template\n");    
    printf("|7.Get Database\n");
    printf("|8.Set Database\n");
    printf("|9.Get Serial Number of Device\n");
	printf("|10.Touch status\n");
	printf("|11.Identify with Touch\n");
    printf("|12.Exit\n");
    printf("------------------------------------\n");
    scanf("%d",&choose_function);  
   
    if(choose_function>=1 && choose_function<=12)   //input range
   	 {
      if(choose_function==1)   //Enrollment
   	   {
   	   	unsigned char enroll_time;
   	   	
   		printf("--Enrollment processing--\n");
   		printf("***Plase press your fingers***\n");

		FP_LED_open();
        if(return_ack != ACK)
          {
           printf("LED_open:No ack\n");
           FP_LED_close();
           return -1;
          }
                                                                                                                    
        FP_EnrollStart(0); 
        if(return_ack != ACK && return_para==0x1005)  //change another IDs if default ID=0 is occupied
          {
           for(loop_time=1;loop_time<=199;loop_time++)  //found another IDs
              {
               FP_EnrollStart(loop_time);
               if(return_ack == ACK)
                 break;
              }  
          }
        
        for(enroll_time=1;enroll_time<=3;enroll_time++)
          {
           printf("Please press %d time and waiting for <taking off finger>message\n",enroll_time);
               
           loop_time=1; 
           while(1)     
             {
				#if (FP_TOUCH ==1) 
			    if(digitalRead(TOUCH_PIN)==HIGH)	 
			    #else
				if(1)	  
		        #endif
			    {
		         FP_CaptureFinger(1);  
				 if(return_ack == ACK)
					{
              		FP_CaptureFinger(1);
              		if(return_ack == ACK)
              			break;              		
					}                

				 delay(10);
				 if(loop_time==500)  //waiting for time out
					{
					printf("Enroll:time out\n");
					FP_LED_close();
					return -1;
					}
				 loop_time++; 
				}
             }   
           
           if(enroll_time<3)
             {       
              FP_Enroll(enroll_time);
              if(return_ack != ACK)
                {
                 printf("Enroll %d:fail!\n",enroll_time);
                 FP_LED_close();
                 return -1;
                }
             
              printf("Take off finger\n");                
              while(1)   //waiting for taking off the finger
                {
                 FP_IsPressFinger();
                 if(return_para == 0x1012)   //finger is not pressed
                   break;
                }                    
             }
           else
              FP_Enroll(enroll_time);
          }
        
        if(return_ack == ACK)   //decide whether enroll ok or fail
          {
           printf("Enroll Finish!\n");
           FP_LED_close();
          } 
        else 
          {
           if(return_para>=0 && return_para<=199)
          	 printf("Duplicated Finger and enroll fail!\n");
           else	
             printf("Enroll fail!\n");
           FP_LED_close();
          }           
       } //exit of enrollment
    
      if(choose_function==2)   //Identify
   	   {
   	    printf("--Identify processing--\n");	
   	    printf("***Plase press your fingers***\n");
   	    FP_LED_open();
        if(return_ack != ACK)
         {
          printf("LED_open:No ack and finish\n");
          FP_LED_close();
          return -1;  
         }
            
        loop_time=1;
        while(1)     //waiting timeout
         {
          #if (FP_TOUCH ==1) 
		  if(digitalRead(TOUCH_PIN)==HIGH)	 //waiting user fingerprint first
		  #else
		  if(1)	
		  #endif
			{	
          	FP_CaptureFinger(0);
          	if(return_ack == ACK)
              {
              FP_CaptureFinger(0);
              if(return_ack == ACK)
             	break;              		
              }    
             
          delay(10);   
          if(loop_time==500)
            {
             printf("Identify:time out and finish!\n");
             FP_LED_close();
             delay(500);
             return -1;
            }
          loop_time++; 
	    	}		  
         }
         
        FP_Identify(); 
        if(return_ack == ACK)
         {
          printf("Identify:OK,ID=%d\n",return_para);
          FP_LED_close(); 
          delay(200);
         }
       else
         {
          printf("Identify:Fail\n");
          FP_LED_close();
          delay(200);
         }  
   	   } // exit of identify

      if(choose_function==3)   //Delete All
       {    	
   	    printf("--Delete All processing--\n");
   	    FP_DeleteAll();  //delete enrolled IDs  
        if(return_ack == ACK)
          printf("DeleteAll:OK\n");
        else
          printf("No template!\n");
       } //exit of Delete all

      if(choose_function==4)   //Get user count
   	   {
   	   	printf("--Get User Count processing--\n");
   	   	FP_GetEnrollCount();
   	   	printf("Enrolled user=%d\n",return_para);
   	   }
   
      if(choose_function==5)   //Get Template
   	   {
   		  unsigned int FP_ID;
   		  printf("--Get Tempalte processing--\n");
   		  printf("please input ID(Enrolled)\n");
   		  scanf("%d",&FP_ID);  
   		  FP_GetTemplate(FP_ID);
   	   } //exit of GetTemplate
   	
      if(choose_function==6)   //Set Template
   	   {
   	      unsigned int FP_ID;
   		  printf("--Set Tempalte processing--\n");
   		  printf("please input ID(Empty)\n");
   		  scanf("%d",&FP_ID);  
   		  FP_SetTemplate(FP_ID);
       } //exit of SetTemplate
   	   
   	  if(choose_function==7)   //Get database
   	   	{
   	   	printf("--Get Database processing--\n");
   	   	FP_GetDatabase();
   	    }
   	   
   	  if(choose_function==8)   //Set database
   	   	{
   	   	printf("--Set Database processing--\n");
   	   	FP_SetDatabase();
   	    }  
   	    	   
   	  if(choose_function==9)   //Set database
   	   	{
   	   	printf("--Get Serail Number of Device--\n");
   	   	FP_DeviceSerialNumber();
   	    }
	  
   	  if(choose_function==10)  //touch status
   	  	{
   	  	printf("--Touch status--\n");
  		#if (FP_TOUCH ==1) 
  			if(digitalRead(TOUCH_PIN)==HIGH)	 //waiting for user's fingerprint first
     			printf("-Touched!\n");
  			else
	 			printf("-No Touch!\n");
  		#else
	 		printf("Please set FP_TOUCH value(definition.h) is 1,\n");
     		printf("and touch pin connected to raspberry\n");
  		#endif
   	  	}
	  
	  if(choose_function==11)  //identify with touch
	  	{
	  	printf("--Identify with touch--\n");
		printf("please press finger:\n");
	  	#if (FP_TOUCH ==1) 
		while(1)
		  {
		   if(digitalRead(TOUCH_PIN)==HIGH)	 
		      break;
		  }
		FP_LED_open();
        if(return_ack != ACK)
          {
          printf("LED_open:No ack and finish\n");
          FP_LED_close();
          return -1;  
          }
            
        loop_time=1;
        while(1)    
         	{
		  	if(digitalRead(TOUCH_PIN)==HIGH)	 
			  {	
          	   FP_CaptureFinger(0);
          	   if(return_ack == ACK)
              	 {
              	 FP_CaptureFinger(0);
              	 if(return_ack == ACK)
             	   break;              		
              	 }    
             
          	   delay(10);   
          	   if(loop_time==500) //waiting timeout
            	 {
            	 printf("Identify:time out and finish!\n");
             	 FP_LED_close();
             	 delay(200);
             	 return -1;
            	 }
          	   loop_time++; 
	    	   }
        	}               
         
        FP_Identify(); 
        if(return_ack == ACK)
          printf("Identify:OK,ID=%d\n",return_para);
        else
          printf("Identify:Fail\n");

		FP_LED_close(); 
        delay(200);
	     		
		#else
		   printf("Please set FP_TOUCH value(definition.h) is 1,\n");
           printf("and touch pin connected to raspberry\n");
		#endif
	  	}
      if(choose_function==12)  //exit menu   	
   	    menu_loop=0;
   	 } //exit of input range

   	else  //error handle of input error range
   	 {     	 
   	  printf("Input error range!\n");
   	  getchar() != '\n';  //clear buffer of scanf
     }
   }//exit of menu handle
} 