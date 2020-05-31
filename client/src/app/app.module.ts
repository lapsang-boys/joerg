import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './nav/navbar/navbar.component';
import { LibraryOverviewComponent } from './library/library-overview/library-overview.component';
import { HomeComponent } from './splashscreen/home/home.component';
import { CardFrontComponent } from './card/card-front/card-front.component';
import { GameLayoutComponent } from './game/layout/game-layout/game-layout.component';
import { PlayerHandComponent } from './game/hand/player-hand/player-hand.component';
import { PlayedCardsComponent } from './game/board/played-cards/played-cards.component';
import { OtherHandsContainerComponent } from './game/hand/other-hands-container/other-hands-container.component';
import { BoardComponent } from './game/board/board/board.component';
import { PlayedCardComponent } from './game/board/played-card/played-card.component';
import { CardExpanderComponent } from './card/card-expander/card-expander.component';

@NgModule({
	declarations: [
		AppComponent,
		NavbarComponent,
		LibraryOverviewComponent,
		HomeComponent,
		CardFrontComponent,
		GameLayoutComponent,
		PlayerHandComponent,
		PlayedCardsComponent,
		OtherHandsContainerComponent,
		BoardComponent,
		PlayedCardComponent,
		CardExpanderComponent
	],
	imports: [
		BrowserModule,
		AppRoutingModule
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule { }
