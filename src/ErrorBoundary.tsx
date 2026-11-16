import { Component, type ReactNode } from 'react';

export default class ErrorBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() {
    if (!this.state.failed) return this.props.children;
    return <main className="panel" role="alert" style={{ maxWidth: 640, margin: '48px auto', padding: 24 }}>
      <h1>Coś poszło nie tak</h1>
      <p>Aplikacja napotkała błąd podczas wyświetlania. Zapisany profil nie został zmieniony.</p>
      <p>Odśwież stronę. Jeśli błąd wraca, w widoku „Mój profil” wyeksportuj profil i usuń go, a następnie zaimportuj poprawioną kopię.</p>
      <button onClick={() => window.location.reload()}>Odśwież stronę</button>
    </main>;
  }
}
