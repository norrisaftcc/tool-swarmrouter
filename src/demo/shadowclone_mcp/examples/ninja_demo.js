#!/usr/bin/env npm start

/**
 * Shadow Clone MCP Demo
 * 
 * This demo shows how the Shadow Clone MCP server works by simulating
 * different types of missions and showing the ninja/clone coordination.
 */

import { MainNinja } from '../lib/ninja.js';

// Create our demo ninja
const sasuke = new MainNinja('Sasuke Uchiha', 'Hidden Leaf Village');

async function runDemo() {
  console.log('🎌 Shadow Clone MCP Demo Starting...\n');
  
  try {
    // Mission 1: Simple task (Shadow Clone Jutsu)
    console.log('='.repeat(60));
    console.log('🎯 MISSION 1: Simple Documentation Task');
    console.log('='.repeat(60));
    
    const mission1 = 'Create documentation for the new API endpoints including authentication, user management, and data retrieval methods';
    const result1 = await sasuke.executeMission(mission1, { maxTokens: 800 });
    
    console.log('\n📊 Mission 1 Results:');
    console.log(`- Jutsu Used: ${result1.mission.result.jutsuType}`);
    console.log(`- Clones Created: ${result1.mission.result.cloneCount}`);
    console.log(`- Success Rate: ${result1.mission.result.successfulClones}/${result1.mission.result.cloneCount}`);
    console.log(`- Token Efficiency: ${result1.mission.result.tokenStats.efficiency}%`);
    console.log(`- Summary: ${result1.summary}\n`);
    
    // Wait a moment before next mission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mission 2: Complex analysis task (Multi Shadow Clone Jutsu)
    console.log('='.repeat(60));
    console.log('🎯 MISSION 2: Complex System Analysis');
    console.log('='.repeat(60));
    
    const mission2 = 'Analyze the entire microservices architecture, identify performance bottlenecks, design scalability improvements, create migration strategy, and plan implementation phases for the next quarter';
    const result2 = await sasuke.executeMission(mission2, { maxTokens: 1200, priority: 'high' });
    
    console.log('\n📊 Mission 2 Results:');
    console.log(`- Jutsu Used: ${result2.mission.result.jutsuType}`);
    console.log(`- Clones Created: ${result2.mission.result.cloneCount}`);
    console.log(`- Success Rate: ${result2.mission.result.successfulClones}/${result2.mission.result.cloneCount}`);
    console.log(`- Token Efficiency: ${result2.mission.result.tokenStats.efficiency}%`);
    console.log(`- Summary: ${result2.summary}\n`);
    
    // Wait a moment before next mission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mission 3: Research task (Clone Network Jutsu)
    console.log('='.repeat(60));
    console.log('🎯 MISSION 3: Information Gathering');
    console.log('='.repeat(60));
    
    const mission3 = 'Research the latest trends in AI development, gather information about new frameworks, collect performance benchmarks, and find case studies from similar projects';
    const result3 = await sasuke.executeMission(mission3, { maxTokens: 900 });
    
    console.log('\n📊 Mission 3 Results:');
    console.log(`- Jutsu Used: ${result3.mission.result.jutsuType}`);
    console.log(`- Clones Created: ${result3.mission.result.cloneCount}`);
    console.log(`- Success Rate: ${result3.mission.result.successfulClones}/${result3.mission.result.cloneCount}`);
    console.log(`- Token Efficiency: ${result3.mission.result.tokenStats.efficiency}%`);
    console.log(`- Summary: ${result3.summary}\n`);
    
    // Wait a moment before next mission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mission 4: Error handling (Dispel Clone Jutsu)
    console.log('='.repeat(60));
    console.log('🎯 MISSION 4: Bug Fix and Cleanup');
    console.log('='.repeat(60));
    
    const mission4 = 'Fix the memory leak in the authentication service and cleanup deprecated code';
    const result4 = await sasuke.executeMission(mission4, { maxTokens: 600 });
    
    console.log('\n📊 Mission 4 Results:');
    console.log(`- Jutsu Used: ${result4.mission.result.jutsuType}`);
    console.log(`- Clones Created: ${result4.mission.result.cloneCount}`);
    console.log(`- Success Rate: ${result4.mission.result.successfulClones}/${result4.mission.result.cloneCount}`);
    console.log(`- Token Efficiency: ${result4.mission.result.tokenStats.efficiency}%`);
    console.log(`- Summary: ${result4.summary}\n`);
    
    // Show final ninja status
    console.log('='.repeat(60));
    console.log('🏆 FINAL NINJA STATUS');
    console.log('='.repeat(60));
    
    const finalStatus = sasuke.getStatus();
    console.log(`🥷 Ninja: ${finalStatus.ninja.name}`);
    console.log(`🏴 Village: ${finalStatus.ninja.village}`);
    console.log(`⭐ Rank: ${finalStatus.ninja.rank}`);
    console.log(`📈 Stats:`);
    console.log(`  - Missions Completed: ${finalStatus.ninja.stats.missionsCompleted}`);
    console.log(`  - Average Efficiency: ${finalStatus.ninja.stats.averageEfficiency.toFixed(1)}%`);
    console.log(`  - Total Tokens Saved: ${finalStatus.ninja.stats.totalTokensSaved}`);
    console.log(`  - Total Clones Created: ${finalStatus.ninja.stats.clonesCreated}`);
    
    // Show mission history
    console.log('\n📜 Recent Mission History:');
    const history = sasuke.getMissionHistory(4);
    history.forEach((mission, index) => {
      console.log(`${index + 1}. ${mission.mission.substring(0, 50)}...`);
      console.log(`   Efficiency: ${mission.result.efficiency}% | Tokens Saved: ${mission.result.tokensSaved}`);
    });
    
    // Demonstrate token efficiency comparison
    console.log('\n='.repeat(60));
    console.log('💰 TOKEN EFFICIENCY DEMONSTRATION');
    console.log('='.repeat(60));
    
    const totalTokensAllocated = 800 + 1200 + 900 + 600; // Sum of all missions
    const totalTokensSaved = finalStatus.ninja.stats.totalTokensSaved;
    const totalEfficiency = (totalTokensSaved / totalTokensAllocated) * 100;
    
    console.log(`📊 Overall Performance:`);
    console.log(`  - Total Tokens Allocated: ${totalTokensAllocated}`);
    console.log(`  - Total Tokens Saved: ${totalTokensSaved}`);
    console.log(`  - Overall Efficiency: ${totalEfficiency.toFixed(1)}%`);
    console.log(`  - Estimated Cost Savings: ${totalEfficiency.toFixed(1)}% reduction in API costs`);
    
    console.log('\n🎉 Demo completed successfully!');
    console.log('💡 The Shadow Clone technique demonstrates efficient task delegation');
    console.log('⚡ Just like in Naruto, multiple clones can work on different parts of a mission simultaneously');
    console.log('🏆 This results in significant token savings while maintaining quality\n');
    
  } catch (error) {
    console.error('❌ Demo failed:', error);
    process.exit(1);
  }
}

// Advanced demo showing different jutsu types
async function advancedJutsuDemo() {
  console.log('\n🔥 ADVANCED JUTSU DEMONSTRATION');
  console.log('='.repeat(60));
  
  const kakashi = new MainNinja('Kakashi Hatake', 'Hidden Leaf Village');
  kakashi.rank = 'Jonin'; // Start as experienced ninja
  
  // Test all jutsu types
  const missions = [
    {
      name: 'Multi Shadow Clone Jutsu',
      mission: 'Analyze complex distributed system architecture and design comprehensive optimization strategy with detailed implementation plan',
      expectedJutsu: 'multi_shadow_clone'
    },
    {
      name: 'Clone Network Jutsu', 
      mission: 'Research market trends and gather competitive intelligence data from multiple sources',
      expectedJutsu: 'clone_network'
    },
    {
      name: 'Transform Clone Jutsu',
      mission: 'Convert legacy XML data format to modern JSON API structure with proper validation',
      expectedJutsu: 'transform_clone'
    },
    {
      name: 'Coordination Jutsu',
      mission: 'Coordinate multiple team outputs and merge different development streams into unified release',
      expectedJutsu: 'coordination'
    }
  ];
  
  for (const { name, mission, expectedJutsu } of missions) {
    console.log(`\n🎯 Testing: ${name}`);
    console.log(`📝 Mission: ${mission.substring(0, 80)}...`);
    
    const result = await kakashi.executeMission(mission, { maxTokens: 1000 });
    const actualJutsu = result.mission.result.jutsuType;
    
    console.log(`✅ Expected: ${expectedJutsu}, Got: ${actualJutsu}`);
    console.log(`⚡ Efficiency: ${result.mission.result.tokenStats.efficiency}%`);
    console.log(`👥 Clones: ${result.mission.result.cloneCount}`);
  }
  
  console.log(`\n🏆 ${kakashi.name} completed advanced jutsu demonstration!`);
  console.log(`📊 Final stats: ${kakashi.stats.averageEfficiency.toFixed(1)}% average efficiency`);
}

// Run the demos
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('🚀 Starting Shadow Clone MCP Demo...\n');
  
  runDemo()
    .then(() => advancedJutsuDemo())
    .then(() => {
      console.log('\n✅ All demos completed successfully!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Demo error:', error);
      process.exit(1);
    });
}