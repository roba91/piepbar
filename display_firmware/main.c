/*
 * main.c
 *
 *  Created on: 01.05.2009
 *      Author: sebastian
 */

#include  <avr/io.h>
#include  <stdlib.h>
#include  <util/delay.h>

#include "include/lc7981.h"
//#include "include/adc.h"
//#include "include/touch.h"



#include "8x8_horizontal_LSB_1.h"
#include "gnulpf.h"
//#include "12x16_horizontal_LSB_2.h"
//#include "button.h"
//#include "writing_demo.h"

uint8_t buffer[800];

void scrub(void) {
	uint8_t color = PIXEL_ON;
	uint8_t x,y;
	while(1) {
		for(y = 0; y <= 80; y++) {
			for(x = 0; x <= 160; x++) {
				lcd_plot_pixel(x,y,color);
				_delay_ms(1);
			}
		}
		color = !color;
	}
}


int main(void) {


	lcd_init(LCD_GRAPHIC);

	lcd_clear();

	lcd_plot_bitmap(0,0,gnulpf,gnulpfWIDTH, gnulpfHEIGHT);

	//scrub();
		/*
	    lcd_plot_text(5,5,"Hello",8,8,font_8x8);
		lcd_plot_pgmtext(50,22,PSTR("World"),8,8,font_8x8);
		lcd_plot_pgmtext(5,40,PSTR("qwertzuiop"),8,8,font_8x8);
		lcd_plot_pgmtext(5,50,PSTR("asdfghjkl"),8,8,font_8x8);
		lcd_plot_pgmtext(5,60,PSTR("yxcvbnm"),8,8,font_8x8);
		*/

	return 0;

}
