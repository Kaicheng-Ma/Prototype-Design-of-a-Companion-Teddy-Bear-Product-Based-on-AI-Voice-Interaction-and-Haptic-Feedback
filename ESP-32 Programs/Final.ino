#include <Wire.h>
#include "Waveshare_LCD1602.h"
#include <FastLED.h>

#define NUM_LEDS 1
#define DATA_PIN 48
#define CLOCK_PIN 13
CRGB leds[NUM_LEDS];

Waveshare_LCD1602 lcd(16,2);  // 16 characters and 2 lines

unsigned long previousMillis = 0;  // 保存上次动作的时间
unsigned long interval = 4000;     // 初始间隔时间为 4-6 秒
bool eyesOpen = true;              // 眼睛状态标志

// Define button and motor control variables
int motor = 12;
float i = 0;
int cnt = 0;
const int buttonPin = 2; // 按钮连接到 D2
int buttonState = HIGH;  // 默认未按下（因为 INPUT_PULLUP）
int lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

// LCD Custom characters
uint8_t bottomOne[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x04, 0x18};
uint8_t bottomTwo[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x04, 0x03};
uint8_t topTwo[8] = {0x18, 0x04, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00};
uint8_t topOne[8] = {0x03, 0x04, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00};
uint8_t longDash[8] = {0x00, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00};
uint8_t topFull[8] = {0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
uint8_t eyeMiddle1[8] = {0x1F, 0x00, 0x00, 0x00, 0x1F, 0x1F, 0x1B, 0x1B};
uint8_t eyeMiddle2[8] = {0x1B, 0x1B, 0x1F, 0x1F, 0x00, 0x00, 0x00, 0x1F};

void setup() {
    Wire.begin();
    lcd.init();
    lcd.customSymbol(0, bottomOne);
    lcd.customSymbol(1, bottomTwo);
    lcd.customSymbol(2, topOne);
    lcd.customSymbol(3, topTwo);
    lcd.customSymbol(4, eyeMiddle1);
    lcd.customSymbol(5, eyeMiddle2);
    lcd.customSymbol(6, longDash);
    lcd.customSymbol(7, topFull);
    randomSeed(analogRead(0));
    openEyes();

    // Setup for motor and LEDs
    pinMode(motor, OUTPUT);
    FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
    Serial.begin(115200);
    pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
    unsigned long currentMillis = millis();
    
    // Handle eye animations independently
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;
        if (eyesOpen) {
            // 25% chance to squeeze eyes, otherwise close them
            if (random(0, 100) < 25) {
                squeezeEyes();
                interval = 3000; // Squeeze eyes last for 3 seconds
            } else {
                closeEyes();
                interval = 600; // Closing eyes last for 0.6 seconds
            }
        } else {
            openEyes();
        }
    }

    // Handle button and motor control
    int reading = digitalRead(buttonPin);
    if (reading != lastButtonState) {
        lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > debounceDelay) {
        if (reading != buttonState) {
            buttonState = reading;
            if (buttonState == LOW) {  // Button pressed
                Serial.println("Button is pressed!");
                cnt++;
            }
        }
    }
    lastButtonState = reading;

    // Motor control based on button state
    if (cnt % 2 != 0) {
        leds[0] = CRGB::Orange;
        FastLED.show();
        Serial.println(cnt);

        i = 0;
        while (i < 22 && cnt % 2 != 0) {  // Check cnt status
            digitalWrite(motor, HIGH);
            delay((0.1 * pow((i - 15), 2) + 22.5) * 4);
            digitalWrite(motor, LOW);
            delay((0.1 * pow((i - 15), 2) + 22.5) * 4);

            i++;
            if (digitalRead(buttonPin) == LOW) {  // Check button during motor operation
                cnt++;
                break;
            }
        }

        digitalWrite(motor, LOW);
        delay(2000);

        leds[0] = CRGB::Blue;
        FastLED.show();

        i = 0;
        while (i < 27 && cnt % 2 != 0) {
            digitalWrite(motor, HIGH);
            delay((0.1 * pow((i - 15), 2) + 22.5) * 4);
            digitalWrite(motor, LOW);
            delay((0.1 * pow((i - 15), 2) + 22.5) * 4);

            i++;
            if (digitalRead(buttonPin) == LOW) {
                cnt++;
                break;
            }
        }

        digitalWrite(motor, LOW);
        delay(1700);
    } else {
        Serial.println("Off");
        Serial.println(cnt);
        leds[0] = CRGB::White;
        FastLED.show();
    }
}
void openEyes() {
    lcd.clear();
    drawEye(0, 4, 5);  // 左眼
    drawEye(13, 4, 5); // 右眼
    interval = random(4000, 6001);  // 更新为维持睁眼 4-6 秒
    eyesOpen = true;
}

void closeEyes() {
    lcd.clear();
    drawClosedEye(0);  // 左眼
    drawClosedEye(13); // 右眼
    eyesOpen = false;
}

void squeezeEyes() {
    lcd.clear();
    drawSqueezeEye(0, false);  // 左眼
    drawSqueezeEye(13, true);  // 右眼（修正颠倒问题）
    eyesOpen = false;
}

void drawEye(int col, int char1, int char2) {
    lcd.setCursor(col, 0);
    lcd.send_string("|");
    lcd.setCursor(col + 1, 0);
    lcd.write_char(char1);
    lcd.setCursor(col + 2, 0);
    lcd.send_string("|");
    lcd.setCursor(col, 1);
    lcd.send_string("|");
    lcd.setCursor(col + 1, 1);
    lcd.write_char(char2);
    lcd.setCursor(col + 2, 1);
    lcd.send_string("|");
}

void drawClosedEye(int col) {
    lcd.setCursor(col, 0);
    lcd.send_string("_");
    lcd.setCursor(col + 1, 0);
    lcd.send_string("_");
    lcd.setCursor(col + 2, 0);
    lcd.send_string("_");
    lcd.setCursor(col, 1);
    lcd.write_char(7);
    lcd.setCursor(col + 1, 1);
    lcd.write_char(7);
    lcd.setCursor(col + 2, 1);
    lcd.write_char(7);
}

void drawSqueezeEye(int col, bool flip) {
    if (!flip) {  // 正常的左眼
        lcd.setCursor(col, 0);
        lcd.write_char(3);
        lcd.setCursor(col + 1, 0);
        lcd.write_char(6);
        lcd.setCursor(col + 2, 0);
        lcd.write_char(1);
        lcd.setCursor(col, 1);
        lcd.write_char(0);
        lcd.setCursor(col + 1, 1);
        lcd.write_char(6);
        lcd.setCursor(col + 2, 1);
        lcd.write_char(2);
    } else {  // 修正后的右眼（上下翻转）
        lcd.setCursor(col, 0);
        lcd.write_char(0);
        lcd.setCursor(col + 1, 0);
        lcd.write_char(6);
        lcd.setCursor(col + 2, 0);
        lcd.write_char(2);
        lcd.setCursor(col, 1);
        lcd.write_char(3);
        lcd.setCursor(col + 1, 1);
        lcd.write_char(6);
        lcd.setCursor(col + 2, 1);
        lcd.write_char(1);
    }
}
//Pint
