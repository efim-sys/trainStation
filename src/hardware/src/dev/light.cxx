#include #include <WiFi.h>
#include <HTTPClient.h>
#include "FS.h"

#include "types.cpp"
using namespace types;

#include "tools.cpp"
using namespace tools;


const char* ssid = "Train-Server";
const char* pass = "be3e5292-d19b-49dc-8180-86faf4e56682";
const char* secr = "2fa93f00-d11f-43d9-b90e-1e61fabdc378";

const u32 in = 3;
const u32 out = 5;
i32 package = 0;


u32 tin, tout;

func IRAM_ATTR out_fn() -> None {
    if (digitalRead(in)) {
        package = 1;
    }
}


func IRAM_ATTR in_fn() -> None {
    if (digitalRead(out)) {
        package = -1;
    }
}


func send(i32 data) -> u32 {
    HTTPClient client;
    Str URI = format("http://192.168.4.1/sensor?secret={}&data={}", {
        std::string(secr),
        std::to_string(data),
    });
    Serial.println(URI.c_str());
    client.begin(URI.c_str());
    return client.GET();
}


func setup() -> None {
    Serial.begin(115200);

    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED) {
        delay(100);
    }

    ledcSetup()
}


func loop() -> None {
    HTTPClient client;
    client.begin("http://192.168.4.1/data?type=people");
    client.GET();

    u32 people = client.getString().toInt();
    analogWrite(15, u32(people * 1.0 / 10 * 1024));


    delay(500);
}
