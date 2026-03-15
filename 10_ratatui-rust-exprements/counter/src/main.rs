use std::io;

use ratatui::{
    DefaultTerminal, Frame,
    style::Stylize,
    symbols::border,
    text::{Line, Span, Text},
    widgets::{Block, Paragraph, Widget},
};

fn main() -> io::Result<()> {
    ratatui::run(|terminal| App::default().run(terminal))
}

#[derive(Debug, Default)]
struct App {
    counter: u8,
    exit: bool,
}

impl App {
    fn run(&mut self, terminal: &mut DefaultTerminal) -> io::Result<()> {
        while !self.exit {
            terminal.draw(|frame| self.draw(frame))?;
            self.handle_events()?;
        }
        Ok(())
    }

    fn draw(&self, frame: &mut Frame) {
        frame.render_widget(self, frame.area());
    }

    fn handle_events(&mut self) -> io::Result<()> {
        Ok(())
    }
}

impl Widget for &App {
    fn render(self, area: ratatui::prelude::Rect, buf: &mut ratatui::prelude::Buffer)
    where
        Self: Sized,
    {
        Paragraph::new(Text::from(vec![Line::from(vec![
            Span::raw("Value: "),
            Span::raw(self.counter.to_string()),
        ])]))
        .centered()
        .block(
            Block::bordered()
                .title(Line::from(" Counter ").bold().centered())
                .title_bottom(
                    Line::from(vec![
                        Span::raw(" Decrement "),
                        Span::raw("<Left>").blue().bold(),
                        Span::raw(" Increment "),
                        Span::raw("<Right>").blue().bold(),
                        Span::raw(" Quit "),
                        Span::raw("<Q>").blue().bold(),
                    ])
                    .centered(),
                )
                .border_set(border::THICK),
        )
        .render(area, buf);
    }
}
