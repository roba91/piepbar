/*
 * lc7981.h
 *
 *  Created on: 01.05.2009
 *      Author: sebastian
 *
 * Version 0.7.1 beta optimized for the kaboard plattform
 *
 * The contents of this file are subject to the Mozilla Public License
 * Version 1.1 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS"
 * basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
 * License for the specific language governing rights and limitations
 * under the License.
 *
 * The Original Code is Sebastians AVR Library for lc7981.
 *
 * The Initial Developer of the Original Code is Sebastian Schumb (webmaster@sebastians-site.de).
 *
 * Contributor(s): None so far.
 *
 * Any version below 0.6 is still licensed under GPL.
 * The GPLed versions will neither be supported, nor developed any further.
 *
 *			'Do the thing you want to do and let your spirits guide you through.
 *			Live a life, worth being remembered.'
 *			-- Remembered - Firewind --
 */


#ifndef LC7981_H_
#define LC7981_H_ LC7981_H_ 	//!< protects this file from beeing double included

#include <avr/io.h>
#include <util/delay.h>
#include <avr/pgmspace.h>

#define LCD_CTRL 		PORTB		//!< Port used for control signals
#define LCD_CRTL_DDR	DDRB 	//!< Data-Direction-Register for the control signals
#define LCD_RS			PB3		//!< Register-Select Pin of the Display
#define LCD_RW			PB2		//!< Read-Write-select Pin
#define LCD_EN			PB1		//!< Strobe Pin


#define LCD_DATA1		PORTC	//!< Port used for data D0 to D4
#define LCD_DATA1_PIN 	PINC	//!< Port used for reading the data D0 to D4
#define LCD_DATA1_DDR	DDRC	//!< Data-Direction-Register for data D0 to D4
#define LCD_DATA1_MASK	0x1F	//!< Mask to get the first 5 bits of a databyte
#define LCD_DATA2		PORTD	//!< Port used for data D5 to D7
#define LCD_DATA2_PIN 	PIND	//!< Port used for reading the data D5 to D7
#define LCD_DATA2_DDR	DDRD	//!< Data-Direction-Register for data D5 to D7
#define LCD_DATA2_MASK	0xE0	//!< Mask to get the last 3 bits of a databyte


// Macros for (un)setting the control pins
#define lcd_rs_high() (LCD_CTRL |= (1 << LCD_RS))	//!< Set the Register-Select pin high
#define lcd_rs_low() (LCD_CTRL &= ~(1 << LCD_RS))	//!< Set the Register-Select pin low

#define lcd_rw_high() (LCD_CTRL |= (1 << LCD_RW))	//!< Set the Read-Write-Select pin high
#define lcd_rw_low() (LCD_CTRL &= ~(1 << LCD_RW))	//!< Set the Register-Select pin low

#define lcd_en_high() (LCD_CTRL |= (1 << LCD_EN))	//!< Set the strobe pin high
#define lcd_en_low() (LCD_CTRL &= ~(1 << LCD_EN))	//!< Set the strobe pin low


#define LCD_TEXT 0				//!< Constant for text mode
#define LCD_TEXT_LINES 10 		//!< Number of lines in text mode
#define LCD_TEXT_COLUMNS 26		//!< Number of columns in text mode

#define LCD_GRAPHIC 1				//!< Constant for graphic mode
#define LCD_GRAPHIC_WIDTH 160		//!< Horizontal display size in pixels
#define LCD_GRAPHIC_HEIGHT 80		//!< Vertical display size in pixels
#define PIXEL_ON 1					//!< see lcd_plot_pixel
#define PIXEL_OFF 0					//!< see lcd_plot_pixel

void lcd_init(uint8_t mode);
void lcd_clear(void);

void lcd_write_text(char *txt);
void lcd_gotoxy(uint8_t x, uint8_t y);

void lcd_plot_pixel(uint8_t x, uint8_t y, uint8_t set);
void lcd_plot_bitmap(uint8_t x, uint8_t y, PGM_P bitmap, uint8_t w, uint8_t h);
//void lcd_plot_bitmap(uint8_t x, uint8_t y, PGM_P bitmap, uint8_t w, uint8_t h);

void lcd_plot_char(uint8_t x, uint8_t y_off, uint8_t c, uint8_t fw, uint8_t fh, PGM_P font);
void lcd_plot_text(uint8_t x, uint8_t y_off, const char *text, uint8_t fw, uint8_t fh, PGM_P font);
void lcd_plot_pgmtext(uint8_t x, uint8_t y_off, PGM_P text, uint8_t fw, uint8_t fh, PGM_P font);


static inline void lcd_strobe(void);
static inline void lcd_write_command(uint8_t cmd, uint8_t data);
static inline uint8_t lcd_read_byte(uint16_t pos);
static inline void lcd_write_byte(uint16_t pos,uint8_t byte);

// Static inline functions, that can be used in the library and in the main programm

/**
 * Generates the strobe signal for writing data.
 * This function is meant for internal usage only.
 */
static inline void lcd_strobe(void) {
	lcd_en_high();
	_delay_us(1);
	lcd_en_low();

}


/**
 *  Writes a command and a data byte to the lcd.
 *
 *  @param cmd the command byte
 *  @param data the data that is going to be written after the command
 */
static inline void lcd_write_command(uint8_t cmd, uint8_t data) {
	_delay_us(30);
	lcd_rw_low();
	lcd_rs_high();
	LCD_DATA1 &= ~LCD_DATA1_MASK;
	LCD_DATA1 |= cmd & LCD_DATA1_MASK;
	LCD_DATA2 &= ~LCD_DATA2_MASK;
	LCD_DATA2 |= cmd & LCD_DATA2_MASK;
	_delay_us(1);
	lcd_strobe();

	lcd_rs_low();
	LCD_DATA1 &= ~LCD_DATA1_MASK;
	LCD_DATA1 |= data & LCD_DATA1_MASK;
	LCD_DATA2 &= ~LCD_DATA2_MASK;
	LCD_DATA2 |= data & LCD_DATA2_MASK;
	_delay_us(1);
	lcd_strobe();

}

/**
 * Reads a byte from the display memory.
 *
 * @param pos 16bit address for display memory
 * @return the byte which has been read
 * @see lcd_gotoxy
 */
static inline uint8_t lcd_read_byte(uint16_t pos) {
uint8_t i,data;

	lcd_write_command(0x0A,(uint8_t) pos );
	lcd_write_command(0x0B,(uint8_t) (pos  >> 8));

	for(i = 0; i < 2; i++) {
		_delay_us(30);
		lcd_rw_low();
		lcd_rs_high();
		LCD_DATA1 &= ~LCD_DATA1_MASK;
		LCD_DATA1 |= 0x0D & LCD_DATA1_MASK;
		LCD_DATA2 &= ~LCD_DATA2_MASK;
		LCD_DATA2 |= 0x0D & LCD_DATA2_MASK;
		_delay_us(1);
		lcd_en_high();

		LCD_DATA1_DDR &= ~LCD_DATA1_MASK;
		LCD_DATA2_DDR &= ~LCD_DATA2_MASK;
		lcd_rs_low();
		lcd_rw_high();
		_delay_us(1);
		data = (uint8_t) (LCD_DATA1_PIN & LCD_DATA1_MASK) | (LCD_DATA2_PIN & LCD_DATA2_MASK);
		lcd_en_low();
		LCD_DATA1_DDR |= LCD_DATA1_MASK;
		LCD_DATA2_DDR |= LCD_DATA2_MASK;
	}
	return data;
}

static inline void lcd_write_byte(uint16_t pos,uint8_t byte) {

	lcd_write_command(0x0A,(uint8_t) pos );
	lcd_write_command(0x0B,(uint8_t) (pos  >> 8));
	lcd_write_command(0x0C,byte);


}





#endif /* LC7981_H_ */