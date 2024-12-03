#define FP_TOUCH 1                   //touch function
#define TOUCH_PIN 1                  

#define FP_MAX_SIZE            200   //fill in fingprint size for GetDatabase and SetDatabase

#define COMMAND_PACKAGE_LENGTH 12    //command package area
#define COMMAND_START_CODE1    0x55
#define COMMAND_START_CODE2    0xAA

#define DATA_PACKAGE_LENGTH    504   //data package area
#define DATA_START_CODE1       0x5A
#define DATA_START_CODE2       0xA5

#define DEVICE_ID	           0x0001

#define OPEN		           0x01  //command define
#define CMOSLED		           0x12
#define GETENROLLCOUNT	       0x20
#define	ENROLLSTART	           0x22
#define CHANGBAUDRATE          0x04
#define ENROLL1		           0x23
#define ENROLL2		           0x24
#define ENROLL3		           0x25
#define ISPRESSFINGER	       0x26
#define DELETEALL	           0x41
#define IDENTIFY	           0x51
#define CAPTURE_FINGER	       0x60
#define GETTEMPLATE            0x70
#define SETTEMPLATE            0x71
#define ACK		               0x30
#define NACK		           0x31

typedef struct {		
	unsigned char Head1;		     
	unsigned char Head2;		     
	unsigned short wDevId;        
	unsigned long	nParam;          
	unsigned short wCmd;          
	unsigned short wChkSum;       
} COMMAND_PACKAGE_STRUCTURE;

typedef struct {		
	unsigned char Head1;		     
	unsigned char Head2;		     
	unsigned short wDevId;        
	unsigned char	nData[498];   
	unsigned short wChkSum;       
} DATA_PACKAGE_STRUCTURE;

extern int serial_var;
unsigned long return_para;    
unsigned short return_ack;    

COMMAND_PACKAGE_STRUCTURE command_package; 
DATA_PACKAGE_STRUCTURE data_package;