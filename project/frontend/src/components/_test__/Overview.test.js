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
import Overview from "../Overview";


// // test
test("render a Home object while not logged in", async() => {
  render(<Overview />);
  // does this object truely exist?
  const isRendered = screen.getByText('Please login');
  expect(isRendered);
});