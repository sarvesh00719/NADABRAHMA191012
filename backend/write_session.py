code = "import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator, Animated } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { fetchApi } from '../../src/api/client';
import { colors } from '../../src/theme/colors';
import { Audio } from 'expo-av';
import * as Speech from 'expo-speech';
import * as SecureStore from 'expo-secure-store';

interface Message { id: string; role: 'user' | 'assistant'; content: string; engine?: string; }

export default function Chat() {
  const { id } = useLocalSearchParams();
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);

  const listRef = useRef<FlatList>(null);
  const waveAnim = useRef(new Animated.Value(1)).current;

  const playSpeech = (textToSpeak: string) => {
    Speech.stop();
    setIsSpeaking(true);
    Speech.speak(textToSpeak, {
      pitch: 1.0,
      rate: 1.0,
      onDone: () => setIsSpeaking(false),
      onError: () => setIsSpeaking(false),
      onStopped: () => setIsSpeaking(false)
    });
  };

  useEffect(() => {
    const fetchMsgs = async () => {
      try {
        const res = await fetchApi(/sessions/ + id + /messages);
        if (res.messages && res.messages.length > 0) {
          setMessages(res.messages);
          const lastMsg = res.messages[res.messages.length - 1];
          if (lastMsg.role === 'assistant') {
            playSpeech(lastMsg.content);
          }
        }
      } catch(e) { console.error(e); }
    };
    fetchMsgs();
    return () => { Speech.stop(); };
  }, [id]);

  useEffect(() => {
    if (isSpeaking) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(waveAnim, { toValue: 1.3, duration: 400, useNativeDriver: true }),
          Animated.timing(waveAnim, { toValue: 1, duration: 400, useNativeDriver: true })
        ])
      ).start();
    } else {
      waveAnim.stopAnimation();
      waveAnim.setValue(1);
    }
  }, [isSpeaking]);

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.status === 'granted') {
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: true,
          playsInSilentModeIOS: true,
        });
        const { recording } = await Audio.Recording.createAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
        setRecording(recording);
        setIsRecording(true);
      }
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  const stopRecording = async () => {
    if (!recording) return;
    setTranscribing(true);
    setIsRecording(false);
    
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);
      
      if (uri) {
        const token = await SecureStore.getItemAsync('token');
        const formData = new FormData();
        formData.append('file', {
          uri,
          name: 'audio.m4a',
          type: 'audio/m4a'
        } as any);

        const response = await fetch(${process.env.EXPO_PUBLIC_API_URL}/sessions/transcribe, {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + token,
          },
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          if (data.text) {
            setText(data.text);
          }
        } else {
          console.error(\"Transcription failed\", await response.text());
        }
      }
    } catch (error) {
      console.error('Failed to stop/transcribe', error);
    } finally {
      setTranscribing(false);
    }
  };

  const sendMessage = async () => {
    if (!text.trim()) return;
    const userMsg = { id: Date.now().toString(), role: 'user' as const, content: text };
    setMessages(prev => [...prev, userMsg]);
    setText('');
    setLoading(true);
    Speech.stop();
    setIsSpeaking(false);
    
    try {
      const res = await fetchApi(/sessions/ + id + /messages, {
        method: 'POST',
        body: JSON.stringify({ text: userMsg.content, client_message_id: userMsg.id })
      });
      setMessages(prev => [...prev, res.assistant_message]);
      playSpeech(res.assistant_message.content);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const endSession = async () => {
    try {
      Speech.stop();
      await fetchApi(/sessions/ + id + /end, { method: 'POST' });
      router.replace(/session/review/ + id);
    } catch (e) {
      console.error(e);
    }
  };

  const renderItem = ({ item }: { item: Message }) => {
    const isUser = item.role === 'user';
    return (
      <View style={[styles.bubble, isUser ? styles.userBubble : styles.botBubble]}>
        <Text style={[styles.msgText, isUser && styles.userMsgText]}>{item.content}</Text>
        {!isUser && item.engine === 'stub' && (
          <Text style={{fontSize: 10, color: '#888', marginTop: 5}}>Offline Fallback</Text>
        )}
        {!isUser && item.engine === 'gemini' && (
          <Text style={{fontSize: 10, color: '#4CAF50', marginTop: 5}}>AI Generated</Text>
        )}
      </View>
    );
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Companion</Text>
        <TouchableOpacity onPress={endSession}><Text style={styles.endText}>End</Text></TouchableOpacity>
      </View>
      
      <FlatList
        ref={listRef}
        data={messages}
        renderItem={renderItem}
        keyExtractor={i => i.id}
        contentContainerStyle={styles.list}
        onContentSizeChange={() => listRef.current?.scrollToEnd()}
      />
      
      {isSpeaking && (
        <View style={styles.waveContainer}>
          <Animated.View style={[styles.waveCircle, { transform: [{ scale: waveAnim }] }]} />
          <View style={styles.waveIcon}><Text style={{fontSize: 20}}>AI</Text></View>
        </View>
      )}

      <View style={styles.inputArea}>
        <TouchableOpacity 
          style={[styles.micBtn, isRecording ? styles.recordingBtn : null]} 
          onPress={isRecording ? stopRecording : startRecording}
          disabled={transcribing || loading}
        >
          {transcribing ? <ActivityIndicator size=\"small\" color=\"#fff\" /> : 
           <Text style={styles.micText}>{isRecording ? \"Stop\" : \"Mic\"}</Text>}
        </TouchableOpacity>
        
        <TextInput
          style={styles.input}
          placeholder=\"Speak or type...\"
          value={text}
          onChangeText={setText}
          multiline
        />
        <TouchableOpacity style={styles.sendBtn} onPress={sendMessage} disabled={loading || isRecording || transcribing}>
          {loading ? <ActivityIndicator color={colors.surface} /> : <Text style={styles.sendBtnText}>Send</Text>}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: { paddingTop: 60, paddingBottom: 15, paddingHorizontal: 20, backgroundColor: colors.surface, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  headerTitle: { fontSize: 18, fontWeight: 'bold', color: colors.text },
  endText: { color: colors.error, fontWeight: 'bold' },
  list: { padding: 20, gap: 10 },
  bubble: { padding: 15, borderRadius: 20, maxWidth: '80%' },
  userBubble: { backgroundColor: colors.chatUser, alignSelf: 'flex-end', borderBottomRightRadius: 5 },
  botBubble: { backgroundColor: colors.chatAssistant, alignSelf: 'flex-start', borderBottomLeftRadius: 5 },
  msgText: { fontSize: 16, color: colors.text },
  userMsgText: { color: colors.surface },
  inputArea: { flexDirection: 'row', padding: 10, paddingBottom: 30, backgroundColor: colors.surface, alignItems: 'center' },
  micBtn: { backgroundColor: '#7b9ee0', padding: 12, borderRadius: 20, marginRight: 10, justifyContent: 'center', alignItems: 'center', width: 60 },
  recordingBtn: { backgroundColor: colors.error },
  micText: { color: colors.surface, fontWeight: 'bold', fontSize: 12 },
  input: { flex: 1, backgroundColor: colors.surface, padding: 12, borderRadius: 20, maxHeight: 100, fontSize: 16, borderWidth: 1, borderColor: colors.border },
  sendBtn: { backgroundColor: colors.primary, padding: 12, borderRadius: 20, marginLeft: 10, justifyContent: 'center', alignItems: 'center', width: 60 },
  sendBtnText: { color: colors.surface, fontWeight: 'bold' },
  waveContainer: { alignItems: 'center', marginBottom: 10, position: 'relative' },
  waveCircle: { width: 40, height: 40, borderRadius: 20, backgroundColor: colors.primary, opacity: 0.3, position: 'absolute', top: 5 },
  waveIcon: { width: 50, height: 50, justifyContent: 'center', alignItems: 'center' }
});"
with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(code)
