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
import Home from "../Home";

// test
test("render a Home object", async() => {
    render(<Home />);
    // does this object truely exist?
    const isTextRendered = screen.getByText('Please login');
    expect(isTextRendered);
  
  })