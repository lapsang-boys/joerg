import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { DragDropModule } from '@angular/cdk/drag-drop'; 

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
import { CardComponent } from './card/card/card.component';
import { CardBackComponent } from './card/card-back/card-back.component';
import { CubeDesignerComponent } from './cube/cube-designer/cube-designer.component';
import { CubeOverviewComponent } from './cube/cube-overview/cube-overview.component';
import { CardCompactComponent } from './card/card-compact/card-compact.component';
import { CubeLibraryComponent } from './cube/cube-library/cube-library.component';

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
		CardExpanderComponent,
		CardComponent,
		CardBackComponent,
		CubeDesignerComponent,
		CubeOverviewComponent,
		CardCompactComponent,
		CubeLibraryComponent
	],
	imports: [
		BrowserModule,
		BrowserAnimationsModule,
		AppRoutingModule,
		DragDropModule,
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule { }
