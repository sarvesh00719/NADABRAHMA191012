import React, { useState, useRef, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator, Animated } from 'react-native';
import { router } from 'expo-router';
import { fetchApi } from '../../src/api/client';
import { useAudioRecorder, useAudioRecorderState, requestRecordingPermissionsAsync, RecordingPresets, createAudioPlayer } from 'expo-audio';
import * as Speech from 'expo-speech';
import * as SecureStore from 'expo-secure-store';
import * as FileSystem from 'expo-file-system/legacy';
import { CameraView, useCameraPermissions } from 'expo-camera';

interface Message { id: string; role: 'user' | 'assistant'; content: string; }

export default function YogaSadhana() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [cameraMode, setCameraMode] = useState(false);
  
  const listRef = useRef<FlatList>(null);
  const waveAnim = useRef(new Animated.Value(1)).current;
  const playerRef = useRef<any>(null);
  const omkarPlayerRef = useRef<any>(null);
  
  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const recordingState = useAudioRecorderState(recorder);

  const [sessionId, setSessionId] = useState('');
  const [permission, requestPermission] = useCameraPermissions();

  useEffect(() => {
    const initSession = async () => {
        try {
            const res = await fetchApi("/sessions", {
                method: "POST",
                body: JSON.stringify({ goal: "yoga_sadhana", language: "en" })
            });
            setSessionId(res.id);
            
            const initialMsg: Message = {
                id: '1', role: 'assistant', 
                content: "Welcome to Yoga Sadhana. I am your Yoga Helper. Let's begin with some Pranayama practices. How is your breathing today?"
            };
            setMessages([initialMsg]);
            playSpeech(initialMsg.content);
        } catch (e) {
            console.error("Failed to create session", e);
        }
    };
    initSession();
    
    return () => {
      Speech.stop();
      if (playerRef.current) playerRef.current.pause();
      if (omkarPlayerRef.current) omkarPlayerRef.current.pause();
    };
  }, []);

  useEffect(() => {
    if (isSpeaking) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(waveAnim, { toValue: 1.3, duration: 800, useNativeDriver: true }),
          Animated.timing(waveAnim, { toValue: 1, duration: 800, useNativeDriver: true })
        ])
      ).start();
    } else {
      waveAnim.stopAnimation();
      waveAnim.setValue(1);
    }
  }, [isSpeaking]);

  const playSpeech = async (textToSpeak: string) => {
    try {
      Speech.stop();
      if (playerRef.current) playerRef.current.pause();
      setIsSpeaking(true);
      
      const apiKey = process.env.EXPO_PUBLIC_ELEVENLABS_API_KEY;
      if (!apiKey) {
        Speech.speak(textToSpeak, { pitch: 1.0, rate: 0.9, onDone: () => setIsSpeaking(false) });
        return;
      }
      
      const voiceId = process.env.EXPO_PUBLIC_ELEVENLABS_VOICE_ID || 'EXAVITQu4vr4xnSDxMaL';
      const url = process.env.EXPO_PUBLIC_API_URL + "/sessions/tts?text=" + encodeURIComponent(textToSpeak) + "&voiceId=" + encodeURIComponent(voiceId) + "&apiKey=" + encodeURIComponent(apiKey);
      
      const player = createAudioPlayer(url);
      playerRef.current = player;
      player.play();
      // Approximate duration since onPlaybackStatusUpdate is complex in SDK 57
      setTimeout(() => setIsSpeaking(false), textToSpeak.length * 60);
    } catch (e) {
      setIsSpeaking(false);
    }
  };

  const startRecording = async () => {
    const { status } = await requestRecordingPermissionsAsync();
    if (status === 'granted') {
      await recorder.prepareToRecordAsync();
      recorder.record();
    }
  };

  const stopRecording = async () => {
    setTranscribing(true);
    try {
      await recorder.stop();
      let uri = recorder.uri;
      if (uri) {
        if (!uri.startsWith('file://') && uri.startsWith('/')) uri = 'file://' + uri;
        const token = await SecureStore.getItemAsync('token');
        const base64Audio = await FileSystem.readAsStringAsync(uri, { encoding: FileSystem.EncodingType.Base64 });
        
        const response = await fetch(process.env.EXPO_PUBLIC_API_URL + "/sessions/transcribe", {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
          body: JSON.stringify({ audio_base64: base64Audio })
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.text) setText(data.text);
        }
      }
    } catch (e) { console.error(e); } 
    finally { setTranscribing(false); }
  };

  const sendMessage = async () => {
    if (!text.trim()) return;
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setText('');
    setLoading(true);
    Speech.stop();
    if (playerRef.current) playerRef.current.pause();
    setIsSpeaking(false);
    
    // We simulate a customized Gemini call by directly asking the backend to generate content, 
    // but we can just use the standard message route and inject a custom system prompt on the backend!
    // For now, let's use the normal route but we append a hidden context.
    try {
      if (!sessionId) return;
      const res = await fetchApi("/sessions/" + sessionId + "/messages", {
        method: 'POST',
        body: JSON.stringify({ text: userMsg.content, client_message_id: userMsg.id })
      });
      setMessages(prev => [...prev, res.assistant_message]);
      playSpeech(res.assistant_message.content);
    } catch (e) { console.error(e); } 
    finally { setLoading(false); }
  };
  
  const startOmkar = () => {
      setCameraMode(true);
      startCamera();
  };
  
  const startCamera = (count: number) => {
      if (count >= 5) {
          setCameraMode(false);
          setOmkarCount(0);
          // Navigate to Lock-in mode or finish
          router.replace('/sahasrara');
          return;
      }
      setOmkarCount(count + 1);
      
      const omkarAsset = process.env.EXPO_PUBLIC_API_URL + '/sessions/sahasrara/omkar';
      const omkarPlayer = createAudioPlayer(omkarAsset);
      omkarPlayerRef.current = omkarPlayer;
      
      const sub = omkarPlayer.addListener('playbackStatusUpdate', (status: any) => {
          if (status.didJustFinish) {
              sub.remove();
              setTimeout(() => startCamera(count + 1), 2000);
          }
      });
      omkarPlayer.play();
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🪷 Sahasrara Focus</Text>
        <TouchableOpacity onPress={() => router.back()}><Text style={styles.endText}>Exit</Text></TouchableOpacity>
      </View>
      
      {cameraMode ? (
          <View style={{flex: 1, backgroundColor: 'black', height: 400}}>
            <CameraView style={{flex: 1}} facing="front" />
            <TouchableOpacity onPress={() => setCameraMode(false)} style={{padding: 20, backgroundColor: '#c0392b', alignItems: 'center'}}>
              <Text style={{color: 'white', fontWeight: 'bold'}}>Stop Camera</Text>
            </TouchableOpacity>
        </View>
      ) : (
          <>
            <FlatList
              ref={listRef}
              data={messages}
              renderItem={({ item }) => {
                const isUser = item.role === 'user';
                // Hide the system prompt injection from UI
                const displayContent = item.content.replace(/\[SYSTEM:.*?\]\s*/g, '');
                return (
                  <View style={[styles.bubble, isUser ? styles.userBubble : styles.botBubble]}>
                    <Text style={[styles.msgText, isUser && styles.userMsgText]}>{displayContent}</Text>
                  </View>
                )
              }}
              keyExtractor={i => i.id}
              contentContainerStyle={styles.list}
              onContentSizeChange={() => listRef.current?.scrollToEnd()}
            />
            
            <View style={styles.omkarBtnContainer}>
                <TouchableOpacity style={styles.omkarStartBtn} onPress={startOmkar}>
                    <Text style={styles.omkarStartText}>Start Yoga Camera 🪷</Text>
                </TouchableOpacity>
            </View>

            <View style={styles.inputArea}>
              <TouchableOpacity 
                style={[styles.micBtn, recordingState.isRecording ? styles.recordingBtn : null]} 
                onPress={recordingState.isRecording ? stopRecording : startRecording}
                disabled={transcribing || loading}
              >
                {transcribing ? <ActivityIndicator size="small" color="#fff" /> : 
                 <Text style={styles.micText}>{recordingState.isRecording ? "Stop" : "Mic"}</Text>}
              </TouchableOpacity>
              
              <TextInput style={styles.input} placeholder="Speak or type..." value={text} onChangeText={setText} multiline />
              <TouchableOpacity style={styles.sendBtn} onPress={sendMessage} disabled={loading || recordingState.isRecording || transcribing}>
                {loading ? <ActivityIndicator color="#121212" /> : <Text style={styles.sendBtnText}>Send</Text>}
              </TouchableOpacity>
            </View>
          </>
      )}
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121212' },
  header: { paddingTop: 60, paddingBottom: 15, paddingHorizontal: 20, backgroundColor: '#1E2A38', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  headerTitle: { fontSize: 18, fontWeight: 'bold', color: '#F39C12' },
  endText: { color: '#e74c3c', fontWeight: 'bold' },
  list: { padding: 20, gap: 10 },
  bubble: { padding: 15, borderRadius: 20, maxWidth: '80%' },
  userBubble: { backgroundColor: '#F39C12', alignSelf: 'flex-end', borderBottomRightRadius: 5 },
  botBubble: { backgroundColor: '#2C3E50', alignSelf: 'flex-start', borderBottomLeftRadius: 5 },
  msgText: { fontSize: 16, color: '#ecf0f1' },
  userMsgText: { color: '#121212' },
  inputArea: { flexDirection: 'row', padding: 10, paddingBottom: 30, backgroundColor: '#1E2A38', alignItems: 'center' },
  micBtn: { backgroundColor: '#34495E', padding: 12, borderRadius: 20, marginRight: 10, justifyContent: 'center', alignItems: 'center', width: 60 },
  recordingBtn: { backgroundColor: '#e74c3c' },
  micText: { color: '#ecf0f1', fontWeight: 'bold', fontSize: 12 },
  input: { flex: 1, backgroundColor: '#2C3E50', color: '#fff', padding: 12, borderRadius: 20, maxHeight: 100, fontSize: 16 },
  sendBtn: { backgroundColor: '#F39C12', padding: 12, borderRadius: 20, marginLeft: 10, justifyContent: 'center', alignItems: 'center', width: 60 },
  sendBtnText: { color: '#121212', fontWeight: 'bold' },
  omkarBtnContainer: { alignItems: 'center', paddingVertical: 10 },
  omkarStartBtn: { backgroundColor: '#9b59b6', paddingHorizontal: 20, paddingVertical: 10, borderRadius: 20 },
  omkarStartText: { color: '#fff', fontWeight: 'bold' },
  omkarContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  lotus: { fontSize: 100, marginBottom: 20 },
  omkarText: { color: '#F39C12', fontSize: 24, fontWeight: 'bold' },
  omkarCount: { color: '#bdc3c7', fontSize: 18, marginTop: 10 }
});
