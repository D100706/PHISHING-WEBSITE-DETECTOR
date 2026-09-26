import React, { useState } from "react";
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    StyleSheet,
} from "react-native";
import axios from "axios";

export default function App() {
    const [url, setUrl] = useState("");
    const [result, setResult] = useState("");

    const checkURL = async() => {
        if (!url.trim()) {
            setResult("Please enter a URL");
            return;
        }

        try {
            const response = await axios.post(
                "http://192.168.31.223:5000/predict", {
                    url: url,
                }
            );

            setResult(response.data.prediction);
        } catch (error) {
            console.log(error);
            setResult("Error connecting to server");
        }
    };

    return ( <
        View style = { styles.container } >
        <
        Text style = { styles.title } > Phishing URL Detector < /Text>

        <
        TextInput style = { styles.input }
        placeholder = "Enter URL"
        value = { url }
        onChangeText = { setUrl }
        autoCapitalize = "none" /
        >

        <
        TouchableOpacity style = { styles.button }
        onPress = { checkURL } >
        <
        Text style = { styles.buttonText } > Check URL < /Text> < /
        TouchableOpacity >

        {
            result !== "" && ( <
                Text style = { styles.result } >
                Prediction: { result } <
                /Text>
            )
        } <
        /View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        padding: 20,
    },

    title: {
        fontSize: 24,
        fontWeight: "bold",
        textAlign: "center",
        marginBottom: 30,
    },

    input: {
        borderWidth: 1,
        borderColor: "#ccc",
        padding: 12,
        borderRadius: 8,
        marginBottom: 20,
    },

    button: {
        backgroundColor: "#007AFF",
        padding: 15,
        borderRadius: 8,
    },

    buttonText: {
        color: "white",
        textAlign: "center",
        fontWeight: "bold",
    },

    result: {
        marginTop: 25,
        textAlign: "center",
        fontSize: 20,
        fontWeight: "bold",
    },
});