/*
  pilightTestPin
  by Sarrailh Remi

  Description : This program test if a Radio receiver is plugged by checking if gpio change
*/

#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>

  int main(int argc, char *argv[]) {
   int pin;
   int received_code;
   int ok_code = 0;
   printf ("Radio 433/315Mhz receiver Test\n");
   printf ("------------------------------\n");

   if(argc == 2) //Verify if there is an argument
   {
      pin = atoi(argv[1]); //Convert first argument to INT
      printf("PIN :%i\n",pin);
    }
  else
    {
      printf("ERROR: No PIN Selected\n");
      exit(1);
    }


    wiringPiSetup();
/* IS PIN RECEIVING RAW DATA */

    printf("TEST : ");
    //We received GPIO State to see if something is happening
    for (int timer = 0; timer < 50; ++timer)
    {
      received_code = digitalRead(pin);
      if (received_code == 1) { ok_code++; } //If PIN IS HIGH add to ok_code
      printf("%i",digitalRead(pin));
      delay(10);
    }

    
    if (ok_code == 0) //If the PIN was never on HIGH we assume there was a problem
    {
      printf("\nSTATE : Not detected \n");
      system("gpio readall");
      exit(1);
    }
    else //If test1 PASS
    {      
      printf("\nSTATE : Detected!\n");
      exit(0);
    }
  }

