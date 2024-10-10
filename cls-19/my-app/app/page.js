"use client";
import Image from "next/image";
import React from "react";

export default function Home() {
  const [count, setCount] = React.useState(0);
  const [data, setData] = React.useState([
    { text: `hello1` },
    { text: `hello2` },
    { text: `hello3` },
    { text: `hello4` },
    { text: `hello5` },
  ]);

  const clicker = () => {
    setCount((prevCount) => prevCount + 1);
  };

  const deletion = (i) => {
    const filteredData = data.filter((_, index) => index !== i);
    setData(filteredData);  // Update state so the component re-renders
  };

  React.useEffect(() => {
    clicker(); // Initial increment
  }, []);

  return (
    <div>
      <button onClick={() => clicker()} className="bg-red-500 w-10 h-10">
        {count}
      </button>
      <div className="text-center">
        {data.map((t, i) => (
          <div key={i} onClick={() => deletion(i)}>
            {t.text}
          </div>
        ))}
      </div>
    </div>
  );
}
