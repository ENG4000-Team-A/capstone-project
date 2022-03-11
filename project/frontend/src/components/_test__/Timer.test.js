// import dependencies
import React from "react";

// import API mocking utilities from Mock Service Worker
import { rest } from "msw";
import { setupServer } from "msw/node";

// import react-testing methods
import { render, fireEvent, waitFor, screen } from "@testing-library/react";

// add custom jest matchers from jest-dom
import "@testing-library/jest-dom";

// component to test
import Timer from "../Timer";


// test
test("render a machine_info object", async() => {
  render(<Timer />);

  // does this object truely exist?
  const isRendered = screen.getByTestId('timer');
  expect(isRendered);

})


