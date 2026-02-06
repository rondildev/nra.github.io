"""
TP 4: Systèmes Embarqués - Système de Surveillance avec Arduino
EST Guelmim - Systèmes Embarqués
Auteur: Nour Eddine AIT ABDALLAH

Code Arduino pour système de monitoring IoT avec capteurs
"""

// Configuration des pins
const int TEMP_SENSOR_PIN = A0;        // Capteur de température
const int HUMIDITY_SENSOR_PIN = A1;    // Capteur d'humidité
const int LIGHT_SENSOR_PIN = A2;       // Capteur de luminosité
const int LED_PIN = 13;                // LED d'indication
const int BUZZER_PIN = 10;             // Buzzer pour alerte

// Seuils d'alerte
const float TEMP_MAX = 35.0;
const float TEMP_MIN = 5.0;
const float HUMIDITY_MAX = 80.0;
const int LIGHT_THRESHOLD = 500;

// Variables pour stockage des données
struct SensorData {
  float temperature;
  float humidity;
  int light;
  unsigned long timestamp;
};

// Historique des lectures
#define HISTORY_SIZE 10
SensorData sensorHistory[HISTORY_SIZE];
int historyIndex = 0;

void setup() {
  // Initialiser la communication série
  Serial.begin(9600);
  
  // Configurer les pins
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Afficher les informations initiales
  Serial.println("=================================");
  Serial.println("Système de Surveillance IoT");
  Serial.println("EST Guelmim - Systèmes Embarqués");
  Serial.println("=================================");
  Serial.println("Démarrage du système...\n");
  
  // Calibrage optionnel des capteurs
  calibrateSensors();
}

void loop() {
  // Lire les capteurs
  SensorData data = readSensors();
  
  // Sauvegarder dans l'historique
  sensorHistory[historyIndex] = data;
  historyIndex = (historyIndex + 1) % HISTORY_SIZE;
  
  // Vérifier les seuils d'alerte
  checkAlerts(data);
  
  // Afficher les données
  displaySensorData(data);
  
  // Envoyer les données au cloud (simulation)
  sendToCloud(data);
  
  // Attendre avant la prochaine lecture
  delay(5000); // Lecture tous les 5 secondes
}

/**
 * Lit les valeurs des capteurs
 */
SensorData readSensors() {
  SensorData data;
  
  // Lire température (capteur LM35)
  // LM35: 10mV par °C
  int tempRaw = analogRead(TEMP_SENSOR_PIN);
  float voltage = (tempRaw / 1023.0) * 5.0;
  data.temperature = voltage * 100.0; // Conversion en °C
  
  // Lire humidité (capteur DHT-like ou humidité relative)
  int humidityRaw = analogRead(HUMIDITY_SENSOR_PIN);
  data.humidity = map(humidityRaw, 0, 1023, 0, 100); // Mapper à 0-100%
  
  // Lire luminosité (LDR)
  data.light = analogRead(LIGHT_SENSOR_PIN);
  
  // Timestamp
  data.timestamp = millis();
  
  return data;
}

/**
 * Vérifie les seuils d'alerte
 */
void checkAlerts(SensorData data) {
  bool alertTriggered = false;
  String alertMessage = "";
  
  // Vérifier température
  if (data.temperature > TEMP_MAX) {
    alertTriggered = true;
    alertMessage += "ALERTE: Température trop élevée! ";
  }
  else if (data.temperature < TEMP_MIN) {
    alertTriggered = true;
    alertMessage += "ALERTE: Température trop basse! ";
  }
  
  // Vérifier humidité
  if (data.humidity > HUMIDITY_MAX) {
    alertTriggered = true;
    alertMessage += "ALERTE: Humidité trop élevée! ";
  }
  
  // Vérifier luminosité
  if (data.light < LIGHT_THRESHOLD) {
    // Lumière insuffisante, activer LED
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  
  // Déclencher buzzer et LED si alerte
  if (alertTriggered) {
    triggerAlarm();
    Serial.println("🚨 " + alertMessage);
  }
}

/**
 * Déclenche l'alarme (son + lumière)
 */
void triggerAlarm() {
  // Bip sonore rapide
  for (int i = 0; i < 5; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);
  }
  
  // Clignoter LED
  for (int i = 0; i < 5; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
  }
}

/**
 * Affiche les données des capteurs
 */
void displaySensorData(SensorData data) {
  Serial.print("Timestamp: ");
  Serial.print(data.timestamp);
  Serial.print("ms | ");
  
  Serial.print("Temp: ");
  Serial.print(data.temperature, 2);
  Serial.print("°C | ");
  
  Serial.print("Humidité: ");
  Serial.print(data.humidity);
  Serial.print("% | ");
  
  Serial.print("Lumière: ");
  Serial.println(data.light);
}

/**
 * Envoie les données au cloud (simulation)
 */
void sendToCloud(SensorData data) {
  // Simulation d'envoi au cloud via WiFi (ESP8266/ESP32)
  // En production, utiliser ThingSpeak, Azure IoT Hub, ou AWS IoT
  
  String payload = "{";
  payload += "\"temperature\":" + String(data.temperature, 2) + ",";
  payload += "\"humidity\":" + String(data.humidity) + ",";
  payload += "\"light\":" + String(data.light) + ",";
  payload += "\"timestamp\":" + String(data.timestamp);
  payload += "}";
  
  // Afficher le payload (en production: envoyer via HTTP/MQTT)
  // Serial.println("📤 Envoi au cloud: " + payload);
}

/**
 * Calibrage des capteurs (optionnel)
 */
void calibrateSensors() {
  Serial.println("Calibrage des capteurs...");
  
  // Lire plusieurs fois pour stabiliser
  for (int i = 0; i < 5; i++) {
    readSensors();
    delay(500);
  }
  
  Serial.println("✓ Calibrage complété\n");
}

/**
 * Affiche l'historique des lectures
 */
void printHistory() {
  Serial.println("\n=== HISTORIQUE DES LECTURES ===");
  for (int i = 0; i < HISTORY_SIZE; i++) {
    int idx = (historyIndex + i) % HISTORY_SIZE;
    Serial.print("Lecture ");
    Serial.print(i + 1);
    Serial.print(" - Temp: ");
    Serial.print(sensorHistory[idx].temperature, 2);
    Serial.print("°C, Humidité: ");
    Serial.print(sensorHistory[idx].humidity);
    Serial.print("%, Lumière: ");
    Serial.println(sensorHistory[idx].light);
  }
}

/**
 * Calcule la moyenne des températures
 */
float calculateAverageTemperature() {
  float sum = 0;
  for (int i = 0; i < HISTORY_SIZE; i++) {
    sum += sensorHistory[i].temperature;
  }
  return sum / HISTORY_SIZE;
}
