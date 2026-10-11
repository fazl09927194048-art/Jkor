import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Activity, ArrowUp, Bot, BrainCircuit, CheckCircle2, Code2, FileText, Image, Mic, Search, Settings2, Sparkles, Video, Wifi, WifiOff } from 'lucide-react';
import './styles.css';

const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const icons = { chat: BrainCircuit, coding: Code2, vision: Image, image_generation: Image, audio: Mic, video: Video, documents: FileText, research: Search };

function App() {
  const [catalog, setCatalog] = useState(null);
  const [messages, setMessages] = useState([{ role: 'assistant', text: 'Welcome to NEXUS AI. I will only show capabilities that are actually configured and reachable. Connect a local Ollama model to begin.' }]);
  const [draft, setDraft] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function refreshCatalog() {
    try {
      const response = await fetch(API + '/api/v1/catalog');
      if (!response.ok) throw new Error('API unavailable');
      setCatalog(await response.json());
    } catch {
      setCatalog(null);
    }
  }
  useEffect(() => { refreshCatalog(); }, []);

  async function sendMessage(event) {
    if (event) event.preventDefault();
    const message = draft.trim();
    if (!message || busy) return;
    setMessages(prev => [...prev, { role: 'user', text: message }]);
    setDraft('');
    setBusy(true);
    setError('');
    try {
      const response = await fetch(API + '/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, ...(selectedModel ? { model: selectedModel } : {}) })
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || 'The model did not respond.');
      setMessages(prev => [...prev, { role: 'assistant', text: payload.text, provider: payload.provider, model: payload.model }]);
      refreshCatalog();
    } catch (err) {
      const note = err.message || 'Could not connect to NEXUS AI API.';
      setError(note);
      setMessages(prev => [...prev, { role: 'assistant', text: 'I could not complete that request: ' + note }]);
    } finally {
      setBusy(false);
    }
  }

  const modelOptions = (catalog?.providers || []).flatMap(provider => (provider.models || []).map(model => ({ id: model, label: provider.label + ' · ' + model })));
  const capabilities = catalog?.capabilities || [
    { id: 'chat', label: 'Chat & reasoning', status: 'needs_provider' },
    { id: 'coding', label: 'Coding assistant', status: 'planned' },
    { id: 'vision', label: 'Image understanding', status: 'planned' },
    { id: 'image_generation', label: 'Image generation', status: 'planned' },
    { id: 'audio', label: 'Audio & voice', status: 'planned' },
    { id: 'video', label: 'Video tools', status: 'planned' },
    { id: 'documents', label: 'Documents & OCR', status: 'planned' },
    { id: 'research', label: 'Web research', status: 'planned' }
  ];

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><Sparkles size={21} /></div><div><strong>NEXUS<span> AI</span></strong><small>ONE WORKSPACE. MANY MINDS.</small></div></div>
      <button className="nav-item active"><BrainCircuit size={18} /> AI Workspace</button>
      <div className="section-label">CAPABILITIES</div>
      {capabilities.map(item => {
        const Icon = icons[item.id] || Bot;
        return <div className="capability" key={item.id}><Icon size={17}/><span>{item.label}</span><i className={item.status === 'available' ? 'dot live' : 'dot'} /></div>;
      })}
      <div className="sidebar-bottom"><div className="provider-card"><div className="provider-title"><Activity size={16}/> Provider status</div><div className="provider-line">{catalog?.providers?.some(p => p.connected) ? <><Wifi size={15} className="green"/> Local model connected</> : <><WifiOff size={15}/> No model connected</>}</div><button onClick={refreshCatalog} className="refresh">Refresh status</button></div><div className="nav-item muted"><Settings2 size={18}/> Settings <span className="soon">SOON</span></div></div>
    </aside>
    <main className="main">
      <header className="topbar"><div><span className="eyebrow">PERSONAL INTELLIGENCE SYSTEM</span><h1>AI Workspace</h1></div><div className="top-actions"><span className="status-pill"><i className={catalog ? 'dot live' : 'dot'} />{catalog ? 'API connected' : 'API offline'}</span><div className="avatar">N</div></div></header>
      <section className="welcome"><div className="orb"><BrainCircuit size={28}/></div><div><h2>Think beyond one model.</h2><p>One interface for your AI tools. Local-first, provider-neutral, transparent.</p></div></section>
      <section className="hub-section"><div className="hub-title"><div><span className="eyebrow">MODEL & TOOL DIRECTORY</span><h2>Capability Hub</h2></div><span className="hub-count">{capabilities.filter(item => item.status === 'available').length} active · {capabilities.length} listed</span></div><div className="capability-grid">{capabilities.map(item => { const Icon = icons[item.id] || Bot; return <div className="capability-card" key={item.id}><div className="capability-card-icon"><Icon size={17}/></div><div className="capability-card-copy"><strong>{item.label}</strong><small>{item.status === 'available' ? 'Ready to use' : item.status === 'needs_provider' ? 'Connect a model' : 'Planned integration'}</small></div><i className={item.status === 'available' ? 'dot live' : 'dot'} /></div>; })}</div></section>
      <section className="chat-panel">
        <div className="chat-heading"><div><strong><Bot size={17}/> NEXUS Assistant</strong><span>Responses are labeled with the real provider and model.</span></div><span className="beta">EARLY ACCESS</span></div>
        <div className="messages">{messages.map((m, i) => <div className={'message ' + m.role} key={i}><div className="message-icon">{m.role === 'assistant' ? <Sparkles size={16}/> : 'Y'}</div><div className="message-body"><p>{m.text}</p>{m.provider && <small className="model-label">{m.provider} · {m.model}</small>}</div></div>)}{busy && <div className="message assistant"><div className="message-icon"><Sparkles size={16}/></div><div className="typing"><i/><i/><i/></div></div>}</div>
        {error && <div className="error-note">{error}</div>}
        <form className="composer" onSubmit={sendMessage}><div className="model-picker"><label htmlFor="model-choice">MODEL</label><select id="model-choice" value={selectedModel} onChange={e => setSelectedModel(e.target.value)}><option value="">Auto / default local model</option>{modelOptions.map(model => <option key={model.id} value={model.id}>{model.label}</option>)}</select><span>{modelOptions.length ? modelOptions.length + ' connected model(s)' : 'No model connected'}</span></div><textarea value={draft} onChange={e => setDraft(e.target.value)} placeholder="Ask anything… (requires a running local model)" rows={2} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } }} /><div className="composer-footer"><span>Enter to send · Shift + Enter for new line</span><button type="submit" disabled={busy || !draft.trim()} aria-label="Send message"><ArrowUp size={18}/></button></div></form>
        <p className="privacy-note"><CheckCircle2 size={14}/> No silent paid fallback. Provider availability is reported honestly.</p>
      </section>
      <footer>NEXUS AI <span>·</span> Modular by design <span>·</span> Build 0.1.0</footer>
    </main>
  </div>;
}

createRoot(document.getElementById('root')).render(<App />);
