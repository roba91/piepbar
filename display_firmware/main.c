/*
 * main.c
 *
 *  Created on: 01.05.2009
 *      Author: sebastian
 */

#include  <avr/io.h>
#include  <stdlib.h>
#include  <util/delay.h>
#include <util/crc16.h>

#include "include/lc7981.h"
#include "include/uart.h"


#include "8x8_horizontal_LSB_1.h"
#include "gnulpf.h"
//#include "12x16_horizontal_LSB_2.h"



int main(void) {

	uart_init();

	lcd_init(LCD_GRAPHIC);

	lcd_clear();

	lcd_plot_bitmap(0,0,gnulpf,gnulpfWIDTH, gnulpfHEIGHT);

	uint8_t buffer[800];
	enum {IDLE, DATA, CRC} state = IDLE;
	enum {UPPER, LOWER} half = UPPER;
	uint16_t count = 0;
	uint16_t crc = 0;
	uint16_t remote_crc = 0;
	uint8_t data;

	while(1) {
		data = uart_getc_timeout();
		if(!uart_timed_out) {
			switch(state) {
				case IDLE:
					if(data == 0xD0) {
						half = UPPER;
						count = 0;
						crc = 0;
						state = DATA;
						uart_putc(0xA0);
					}
					else if(data == 0xD1) {
						half = LOWER;
						count = 0;
						crc = 0;
						state = DATA;
						uart_putc(0xA1);
					}
					break;

				case DATA:
					buffer[count] = data;
					crc = _crc16_update(crc, data);
					count++;
					if(count >= 400) {
						state = CRC;
						count = 0;
					}
					break;

				case CRC:
					if(count == 0) {
						remote_crc = data << 8;
						count++;
					}
					else {
						remote_crc |= data;
						
						if(remote_crc == crc) {
							if(half == UPPER) {
								uart_putc(0xAA);
							}
							else {
								uart_putc(0xAB);
							}
						}
						for(count = 0; count <= 400; count++) {
							lcd_write_byte(count, buffer[count]); 
						}
						state = IDLE;
					}
					break;

				default:
					break;
			}
		}
		else {
			state = IDLE;
			count = 0;
			crc = 0;

		}
	}


	return 0;

}
