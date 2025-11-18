"""MediaVideo component."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class MediaVideo:
    """A media video component."""

    text: str
    variant: str
    state: str

    def __call__(self) -> Node:
        """Render the component as HTML with enhanced structure."""
        return html(t"""
            <div class="media-video-container">
                <div class="video-wrapper {self.variant}" data-state={self.state}>
                    <div class="video-player">
                        <video class="video-element">
                            <source src="video.mp4" type="video/mp4" />
                        </video>
                        <div class="video-overlay">
                            <div class="video-controls">
                                <button class="play-btn">Play</button>
                                <div class="progress-bar">
                                    <div class="progress-fill"></div>
                                </div>
                                <button class="volume-btn">Volume</button>
                                <button class="fullscreen-btn">Fullscreen</button>
                            </div>
                        </div>
                    </div>
                    <div class="video-info">
                        <h4 class="video-title">{self.text}</h4>
                        <div class="video-metadata">
                            <span class="video-duration">0:00</span>
                            <span class="video-views">0 views</span>
                        </div>
                    </div>
                </div>
            </div>
        """)
