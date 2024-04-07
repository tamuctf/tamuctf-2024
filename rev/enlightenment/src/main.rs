use std::time::Duration;
use hex_literal::hex;
use rand::{Rng, SeedableRng};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tokio::time::sleep(Duration::from_secs(120)).await;

    let mut rng = rand_chacha::ChaChaRng::from_seed(hex!("cc33749278a1a92ed5220a3fd23cde0254374fdb9d8fb326f26fe8c1201dae37"));
    let mut filename = [0u8; 64];
    rng.fill(&mut filename);

    let url = format!("https://cdn.discordapp.com/attachments/811639106576318555/1226243329247678554/{}?ex=66240f18&is=66119a18&hm=bd918f9b7127f4c9aabe5b2283976d1e6dc9f7d8dadedcdfedf79683b212b756&", hex::encode(&filename));
    let _ = reqwest::get(url).await;

    Ok(())
}
