#ifndef UART_H_
#define UART_H_ UART_H_

#include  <avr/io.h>
#include  <stdlib.h>
#include  <util/delay.h>


#define BAUD 115200UL		// baudrate
#define UART_TIMEOUT 250 	// Timeout in ms

// Some calculations ...
#define UBRR_VAL ((F_CPU+BAUD*8)/(BAUD*16)-1)   // Rounding magic
#define BAUD_REAL (F_CPU/(16*(UBRR_VAL+1)))     // Real baudrate
#define BAUD_ERROR ((BAUD_REAL*1000)/BAUD)		// Error in 0,1%

#if ((BAUD_ERROR<950) || (BAUD_ERROR>1050))		// Make sure your UBRR_VAL will work
  #error Baudrate error is bigger then 1% !
#endif

static uint8_t uart_timed_out = 0;

static inline void uart_init(void) {
	UBRRH = UBRR_VAL >> 8;		//Setting baudrate
	UBRRL = UBRR_VAL & 0xFF;

	UCSRB |= (1<<TXEN) | (1<<RXEN);  // UART TX
	UCSRC = (1<<URSEL)|(1<<UCSZ1)|(1<<UCSZ0);  // Asynchronous 8N1
}

static inline void uart_putc(uint8_t data) {
	UDR = data;						// write byte to data register
	while (!(UCSRA & (1<< TXC))); 	// waiting for the uart to finish transmission
	UCSRA |= (1 << TXC); 
}

static inline uint8_t uart_getc(void) {
	while (!(UCSRA & (1<<RXC)));
	return UDR;
}

static inline uint8_t uart_getc_timeout(void) {
	uint8_t retries = UART_TIMEOUT;
	uint8_t delays = 0;

	while (!(UCSRA & (1<<RXC)) && (retries > 0)) {
		if(delays == 0) {
			retries--;
		}
		delays = (delays + 1) % 250;
		_delay_us(4);
	}

	if(retries > 0) {
		uart_timed_out = 0;
		return UDR;
	}

	uart_timed_out = 1;
	return 0;
}



#endif