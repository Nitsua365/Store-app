extern crate sxd_document;
extern crate sxd_xpath;

use std::string;

use sxd_xpath::evaluate_xpath;

pub extern fn parseXPath(doc: String, xpath: String) -> String {
  let docPack = sxd_document::parser::parse(&doc).expect("failed to parse XML doc");
  let document = docPack.as_document();

  let parse_path = evaluate_xpath(
    &document, 
    "//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*")
    .expect("XPath processing failed");


  return parse_path.string();
}