import logo from "./logo.svg";
import "./App.css";
import { useState, useEffect } from "react";
import { getDefaultNormalizer } from "@testing-library/react";

function App() {
  const [text, setText] = useState("random title");

  const [isLoading, setIsLoading] = useState(false);

  //TODO: Learn useReducer
  //TODO: Learn userContext
  //TODO: Learn useFetch(custom function, not part of react)
  //TODO: Learn PropType
  //TODO: Learn Router
  //TODO: Learn useCallback

  const url = " ";

  const getData = async () => {
    //fetch data from api
    fetch(url)
      .then((resp) => resp.json())
      .then((user) => {
        const { login } = user;
        setText("sometext");
        setIsLoading(false);
      })
      .catch((error) => console.log(error));
  };

  useEffect(() => {
    //called everytime rendered
    console.log("call useEffect()");
    getData(); //get data first thing once rendered
  }, []); //aSdd an array to run only once

  const books = [{ id: 1, title: "What is love", author: "Anon" }];

  const Book = ({ title, author }) => {
    const clickHandler = (author) => {
      alert("hello world");
      alert(author + "clicked");
    };
    return (
      <article>
        <h1> {title}</h1>
        <h1> {author}</h1>
        <button type="button" onClick={() => clickHandler(author)}>
          View book
        </button>
      </article>
    );
  };

  function bookList() {
    return books.map((book, index) => {
      return <Book key={book.id} {...book}></Book>;
    });
  }

  const usestatedemo = () => {
    setIsLoading(false);
    setText("hello world");
  };

  if (isLoading) {
    return (
      <div>
        <h4>Loading...</h4>
      </div>
    );
  }

  return (
    <div>
      <section>{bookList()}</section>
      <h1>{text}</h1>
      <button onClick={usestatedemo}> usestate function </button>
    </div>
  );
}

export default App;
