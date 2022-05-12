import { Flex, Heading, Text, Grid, GridItem } from "@chakra-ui/react"
import React from "react";

const Imprint = () => {

    return (
        <Flex flexDir="column" flexGrow={1}>
            <Heading p='5'>Imprint</Heading>
            <Grid
                h='100%'
                templateRows='repeat(3, 1fr)'
                templateColumns='repeat(1, 1fr)'
                gap={5}
                color='gray.600'
                p='5'
            >
                <GridItem rowSpan={2} colSpan={1} p='5' boxShadow='md' rounded='md' bg='gray.200'>
                    <Text>
                        <b>Angaben gemäß § 5 TMG</b>
                        <br></br>
                        <br></br>
                        Max Muster
                        <br></br>
                        Musterweg
                        <br></br>
                        12345 Musterstadt
                        <br></br>
                        <br></br>
                        Vertreten durch:
                        <br></br>
                        Max Mustermann
                        <br></br>
                        <br></br>
                        Kontakt:
                        <br></br>
                        Telefon: 01234-789456
                        <br></br>
                        Fax: 1234-56789
                        <br></br>
                        E-Mail: max@muster.de
                        <br></br>
                    </Text>
                </GridItem>
                <GridItem rowSpan={2} colSpan={1} p='5' boxShadow='md' rounded='md' bg='gray.200'>
                    <b>Haftung für Links</b>
                    <br></br>
                    <br></br>
                    Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar. Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend entfernen.
                </GridItem>
                <GridItem rowSpan={2} colSpan={1} p='5' boxShadow='md' rounded='md' bg='gray.200'>
                    <b>Urheberrecht</b>
                    <br></br>
                    <br></br>
                    Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet. Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die Urheberrechte Dritter beachtet. Insbesondere werden Inhalte Dritter als solche gekennzeichnet. Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Inhalte umgehend entfernen.
                </GridItem>
            </Grid>

        </Flex>
    )
}

export default Imprint;