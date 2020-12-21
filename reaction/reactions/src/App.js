import logo from './logo.svg';
import './App.css';
import React from 'react';

class Panel extends React.Component {
  constructor(props) {
    super(props);
    this.state = { start_time: 0, ran_once: false, counting: false, true_duration: 0, reaction_time: 0, color: 'green' };
    this.process_click = this.process_click.bind(this);
  }
  handle_color = (c) => {
    // TODO: Your code here!
    let msg_res = "Hello World!"
    if(this.state.counting && c === 'darkred') msg_res= "Wait for Green"
    else if (this.state.counting && c === 'green') msg_res = "Click!"
    else if(this.state.ran_once) msg_res = `Your reaction time is ${this.state.reaction_time} ms`
    else msg_res = "Click me to begin!"

    if(c === "darkred")
    {
      setTimeout(function(){
        this.setState({color:'green'})
      }.bind(this), this.state.true_duration);
    }

    return msg_res;
  }
  async start_count() {
    // TODO: Your code here!
    let new_duration = Math.floor(2000 + Math.random() * 5000)
    this.setState({
      start_time: window.performance.now(), true_duration: new_duration,
      counting: true, color: 'darkred'
    })
    
    console.log(`time: ${new_duration}`) //LOG
  }
  end_count() {
    // TODO: Your code here!  
    let elapsed = Math.floor(window.performance.now() - this.state.start_time)
    if(elapsed >= this.state.true_duration)
    {
      this.setState({ran_once: true, counting: false, reaction_time: elapsed-this.state.true_duration})
    }
  }
  process_click() {
    if (this.state.counting && this.state.color === 'green') {
      this.end_count();
    } else if(this.state.color === 'green') this.start_count();
  }
  render() {
    
    // TODO: Your code here!
    let msg = this.handle_color(this.state.color)

    console.log(`msg: ${msg}`)
    return (
      <div className="PanelContainer" onClick={this.process_click} style={{ background: this.state.color }}>
        <div className="Panel">{msg}</div>
      </div>
    );
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1 className="Header">How Fast is your Reaction Time?</h1>
        <Panel />
        <p>Click as soon as the red box turns green. Click anywhere in the box to start.</p>
      </header>
    </div>
  );
}

export default App;
