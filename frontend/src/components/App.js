import React, { Component } from "react";
import { render } from "react-dom";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/music")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  onClick = e => {
    if (this.audio) {
      this.audio.pause();
    }
    this.audio = new Audio(e.target.dataset.url);
    this.audio.play();
  }
  render() {
    return (
      <div className='container'>
        {this.state.data.map(contact => {
          return (
            <div key={contact.id}>
                <img src={contact.image}></img>
                <h4>{contact.name}</h4>
                <h4>{contact.author}</h4>
                <button onClick={this.onClick} data-url={contact.audio}>Play</button>
            </div>
          );
        })}
      </div>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);